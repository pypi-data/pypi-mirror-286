import json
import os
import tempfile
import time
import zipfile
from datetime import datetime
from typing import Literal

import bugsnag
import jwt
import pytz
import requests
import typer
import yaml
from tenacity import retry, stop_after_delay, wait_fixed
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper
from tzlocal import get_localzone

from cerebrium.config import CerebriumConfig
from cerebrium.files import INTERNAL_FILES
from cerebrium.types import JSON
from cerebrium.utils.logging import cerebrium_log, logger
from cerebrium.utils.project import get_current_project_context
from cerebrium.utils.sync_files import make_cortex_dep_files

ENV = os.getenv("ENV", "prod")

if ENV == "local":
    api_url_v2 = os.getenv("REST_API_URL", "http://localhost:4100")
    auth_url = os.environ.get(
        "AUTH_URL",
        "https://dev-cerebrium.auth.eu-west-1.amazoncognito.com/oauth2/token",
    )
    client_id = os.environ.get("CLIENT_ID", "207hg1caksrebuc79pcq1r3269")
    dashboard_url = "http://localhost:4100"
elif ENV == "dev":
    api_url_v1 = os.getenv("REST_API_URL", "https://dev-rest-api.cerebrium.ai")
    api_url_v2 = os.getenv("REST_API_URL", "https://dev-rest.cerebrium.ai")
    auth_url = os.environ.get(
        "AUTH_URL",
        "https://dev-cerebrium.auth.eu-west-1.amazoncognito.com/oauth2/token",
    )
    client_id = os.environ.get("CLIENT_ID", "207hg1caksrebuc79pcq1r3269")
    dashboard_url = "https://dev-dashboard.cerebrium.ai"
else:
    api_url_v1 = os.getenv("REST_API_URL", "https://rest-api.cerebrium.ai")
    api_url_v2 = os.getenv("REST_API_URL", "https://rest.cerebrium.ai")
    auth_url = os.environ.get(
        "AUTH_URL",
        "https://prod-cerebrium.auth.eu-west-1.amazoncognito.com/oauth2/token",
    )
    client_id = os.environ.get("CLIENT_ID", "2om0uempl69t4c6fc70ujstsuk")
    dashboard_url = "https://dashboard.cerebrium.ai"


def is_logged_in() -> str | None:
    """
    Check if a user's JWT token has expired. If it has, make a request to Cognito with the refresh token to generate a new one.

    Returns:
        str: The new JWT token if the old one has expired, otherwise the current JWT token.
    """
    # Assuming the JWT token is stored in a config file
    config_path = os.path.expanduser("~/.cerebrium/config.yaml")
    if not os.path.exists(config_path):
        cerebrium_log(
            level="ERROR",
            message="You must log in to use this functionality. Please run 'cerebrium login'",
            prefix="",
        )
        bugsnag.notify(Exception("User not logged in"))
        return None

    with open(config_path, "r") as f:
        config = yaml.safe_load(f) or {}

    if config is None:
        cerebrium_log(
            level="ERROR",
            message="You must log in to use this functionality. Please run 'cerebrium login'",
            prefix="",
        )
        bugsnag.notify(Exception("User not logged in"))
        return None

    key_name = "" if ENV == "prod" else f"{ENV}-"

    jwt_token: str = config.get(f"{key_name}accessToken", "")
    refresh_token: str = config.get(f"{key_name}refreshToken", "")
    if not jwt_token:
        cerebrium_log(
            level="ERROR",
            message="You must log in to use this functionality. Please run 'cerebrium login'",
            prefix="",
        )
        return None

    # Decode the JWT token without verification to check the expiration time
    try:
        payload = jwt.decode(jwt_token, options={"verify_signature": False})
    except Exception as e:
        cerebrium_log(level="ERROR", message=f"Failed to decode JWT token: {str(e)}", prefix="")
        bugsnag.notify(Exception("Failed to decode JWT token."))
        return None  # Check if the token has expired
    if datetime.fromtimestamp(payload["exp"]) < datetime.now():
        # Token has expired, request a new one using the refresh token
        response = requests.post(
            auth_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "refresh_token",
                "client_id": client_id,
                "refresh_token": refresh_token,
            },
        )
        if response.status_code == 200:
            new_jwt_token = response.json()["access_token"]
            # Update the config file with the new JWT token
            config[f"{key_name}accessToken"] = new_jwt_token
            with open(config_path, "w") as f:
                yaml.safe_dump(config, f)
            return new_jwt_token
        else:
            cerebrium_log(
                level="ERROR",
                message="Failed to refresh JWT token. Please login again.",
                prefix="",
            )
            bugsnag.notify(Exception("Failed to refresh JWT token."))
            return None
    else:
        # Token has not expired, return the current JWT token
        return jwt_token


@retry(stop=stop_after_delay(60), wait=wait_fixed(8))
def cerebrium_request(
    http_method: Literal["GET", "POST", "DELETE", "PATCH"],
    url: str,
    payload: dict[str, JSON] = {},
    requires_auth: bool = True,
    headers: dict[str, str] = {"ContentType": "application/json"},
    v1: bool = False,
) -> requests.Response:
    """
    Make a request to the Cerebrium API and check the response for errors.

    Args:
        http_method ('GET', 'POST', 'DELETE'): The HTTP method to use (GET, POST or DELETE).
        url (str): The url after the base url to use.
        payload (dict, optional): The payload to send with the request.
        requires_auth (bool): If the api call requires the user to be authenticated
        headers (dict, optional): By default, content-type is application/json so this is used to override
        v1 (bool, optional): If the request is to the v1 API. Defaults to False.

    Returns:
        dict: The response from the request.
    """
    if requires_auth:
        access_token = is_logged_in()
        if not access_token:
            raise Exception("User is not logged in")

        payload["projectId"] = get_current_project_context()

    else:
        access_token = None

    url = f"{api_url_v1 if v1 else api_url_v2}/{url}"

    if access_token:
        headers["Authorization"] = f"{access_token}"

    data = None if payload is None else json.dumps(payload)
    if http_method == "POST":
        resp = requests.post(url, headers=headers, data=data, timeout=30)
    elif http_method == "GET":
        resp = requests.get(
            url,
            headers=headers,
            params=payload,
            timeout=30,
        )
    elif http_method == "DELETE":
        resp = requests.delete(url, headers=headers, params=payload, data=data, timeout=30)
    elif http_method == "PATCH":
        resp = requests.patch(url, headers=headers, params=payload, data=data, timeout=30)
    else:
        cerebrium_log(
            level="ERROR",
            message="Invalid HTTP method. Please use 'GET', 'POST', 'DELETE' or 'PATCH'.",
            prefix="",
        )
        bugsnag.notify(Exception("Invalid HTTP method."))
        raise typer.Exit(1)
    return resp


def upload_cortex_files(
    upload_url: str,
    zip_file_name: str,
    config: CerebriumConfig,
    file_list: list[str],
    source: Literal["serve", "cortex"] = "cortex",
    disable_animation: bool = False,
) -> bool:
    if file_list == []:
        cerebrium_log(
            level="ERROR",
            message="No files to upload.",
            prefix="Error uploading app to Cerebrium:",
        )
        return False

    # Zip all files in the current directory and upload to S3
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, zip_file_name)
        make_cortex_dep_files(working_dir=temp_dir, config=config)
        tmp_dep_files = os.listdir(temp_dir)
        with zipfile.ZipFile(zip_path, "w") as zip_file:
            print(f"🗂  Zipping {len(file_list)} file(s)...")
            for f in tmp_dep_files:
                if not disable_animation:
                    print(f"⥅ Creating dependency file {f}")
                zip_file.write(os.path.join(temp_dir, f), arcname=os.path.basename(f))

            for f in file_list:
                if os.path.basename(f) in INTERNAL_FILES:
                    if not disable_animation:
                        print(f"⛔️ Skipping conflicting dependency file {f}")
                        print(
                            f"ℹ  Ensure dependencies in `{f}` are reflected in `cerebrium.toml`"
                        )
                    continue
                if not disable_animation:
                    print(f"＋ Adding {f}")
                if os.path.isfile(f):
                    zip_file.write(f)
                elif os.path.isdir(f) and len(os.listdir(f)) == 0:
                    zip_file.write(f, arcname=os.path.basename(f))

        print("⬆️ Uploading to Cerebrium...")

        with open(zip_path, "rb") as f:
            headers = {
                "Content-Type": "application/zip",
            }
            if not disable_animation:
                with tqdm(
                    total=os.path.getsize(zip_path),
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                    colour="#EB3A6F",
                ) as pbar:  # type: ignore
                    wrapped_f = CallbackIOWrapper(pbar.update, f, "read")
                    upload_response = requests.put(
                        upload_url,
                        headers=headers,
                        data=wrapped_f,  # type: ignore
                        timeout=60,
                    )
            else:
                upload_response = requests.put(
                    upload_url,
                    headers=headers,
                    data=f,
                    timeout=60,
                )

        if upload_response.status_code != 200:
            bugsnag.notify(
                Exception(f"Error uploading app to Cerebrium\n{upload_response.json()}")
            )
            cerebrium_log(
                level="ERROR",
                message=f"Error uploading app to Cerebrium\n{upload_response.json().get('message')}",
                prefix="",
            )
            return False
        if source == "cortex":
            print("✅ Resources uploaded successfully.")
        return True


def log_build_status(
    build_status: str,
    start_time: float,
    mode: Literal["build"] | Literal["serve"] = "build",
) -> str:
    # Status messages mapping
    status_messages = {
        "building": "🔨Building App...",
        "initializing": "🛠️Initializing...",
        "synchronizing_files": "📂Syncing files...",
        "serving": "⏰Waiting for requests...",
        "pending": "⏳Build pending...",
        "failed": "🚨Build failed!",
    }

    # Default message
    msg = status_messages.get(build_status, str(build_status).replace("_", " ").capitalize())
    if build_status == "None":
        msg = "waiting for build status..."

    if build_status == "Success" and mode == "serve":
        msg = "⏰Waiting for requests..."

    if build_status == "pending" and time.time() - start_time > 20:
        msg = "⏳Build pending...trying to find hardware"

    return msg


def poll_build_logs(build_id: str, app_name: str, interval: int = 2):
    """
    Polls logs at specified intervals and prints only new log lines.

    Args:
        build_id (str): The unique identifier of the build
        app_name (str): The name of the app being deployed
        interval (int): The interval in seconds between polls. Defaults to 2 seconds.
    """
    seen_logs = set()
    build_status = "building"

    while build_status not in ["success", "build_failure", "init_failure"]:
        project_id = get_current_project_context()
        logs_response = cerebrium_request(
            "GET",
            f"v2/projects/{project_id}/apps/{project_id}-{app_name}/builds/{build_id}/logs",
            {},
        )
        if logs_response is None:
            bugsnag.notify(Exception("Error streaming logs"))
            cerebrium_log(
                level="ERROR",
                message="Error streaming logs. Please check your internet connection and ensure you are logged in. If this issue persists, please contact support.",
            )
            exit()

        if logs_response.status_code != 200:
            bugsnag.notify(Exception(f"Error streaming logs\n{logs_response.json()}"))
            cerebrium_log(
                level="ERROR",
                message=f"Error streaming logs\n{logs_response.json().get('message')}",
                prefix="",
            )
            exit()

        if logs_response.status_code == 200:
            build_status = logs_response.json()["status"]
            current_log_lines = logs_response.json()["logs"]

            # Process each log line
            for log_entry in current_log_lines:
                created_at = format_created_at(log_entry.get("createdAt"))
                log_text = log_entry.get("log")
                log_key = (created_at, log_text)  # Create a hashable key

                if log_key not in seen_logs:
                    if "error" in log_text.lower():
                        logger.error(f"{created_at} {log_text}")
                    else:
                        logger.info(f"{created_at} {log_text}")
                    seen_logs.add(log_key)

        time.sleep(interval)

    return build_status


def format_created_at(created_at: str):
    # Convert the string timestamp to a datetime object
    utc_time = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Get the local timezone
    local_tz = get_localzone()

    # Convert the UTC time to local time
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_tz)

    # Format the local time nicely
    nice_format = local_time.strftime("%H:%M:%S")

    return nice_format
