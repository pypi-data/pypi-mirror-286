import os
import sys
from typing import Any, Tuple, Dict

import typer
from rich.live import Live
from rich.spinner import Spinner

from cerebrium import __version__
from cerebrium.api import (
    cerebrium_request,
    upload_cortex_files,
    poll_build_logs,
)
from cerebrium.config import CerebriumConfig
from cerebrium.types import LogLevel
from cerebrium.utils.display import confirm_deployment
from cerebrium.utils.files import determine_includes
from cerebrium.utils.logging import cerebrium_log, console
from cerebrium.utils.project import get_current_project_context
from cerebrium.utils.termination import _graceful_shutdown
from cerebrium.utils.verification import run_pyflakes

ENV = os.getenv("ENV", "prod")


def _setup_request(
    payload: dict,
) -> dict[str, Any]:
    project_id = get_current_project_context()
    setup_response = cerebrium_request("POST", f"v2/projects/{project_id}/apps", payload)
    if setup_response is None:
        cerebrium_log(
            level="ERROR",
            message="❌ There was an error deploying your app. Please login and try again. If the error continues to persist, contact support.",
            prefix="",
        )
        exit()

    if setup_response.status_code != 200:
        cerebrium_log(
            message=f"❌ There was an error deploying your app\n{setup_response.json()['message']}",
            prefix="",
            level="ERROR",
        )
        exit()
    print("✅ Initial app configuration complete.")

    return setup_response.json()


def package_app(
    config: CerebriumConfig,
    force_rebuild: bool,
    init_debug: bool,
    disable_build_logs: bool,
    log_level: LogLevel,
    disable_syntax_check: bool,
    disable_animation: bool,
    disable_confirmation: bool,
) -> Tuple[str, Dict[str, Any]]:
    # Get the files in the users directory
    file_list = determine_includes(
        include=config.deployment.include,
        exclude=config.deployment.exclude,
    )
    if file_list == []:
        cerebrium_log(
            "⚠️ No files to upload. Please ensure you have files in your project.",
            level="ERROR",
        )
        raise typer.Exit()

    if "./main.py" not in file_list and "main.py" not in file_list:
        cerebrium_log(
            "⚠️ main.py not found. Please ensure your project has a main.py file.",
            level="ERROR",
        )
        raise typer.Exit()

    if not disable_syntax_check:
        run_pyflakes(files=file_list, print_warnings=True)

    if not disable_confirmation:
        if not confirm_deployment(config):
            sys.exit()

    payload = config.to_payload()
    payload["forceRebuild"] = force_rebuild
    payload["initDebug"] = init_debug
    payload["logLevel"] = log_level
    payload["disableBuildLogs"] = disable_build_logs
    payload["cliVersion"] = __version__

    setup_response = _setup_request(
        payload,
    )

    build_id = setup_response["buildId"]
    print(f"🆔 Build ID: {build_id}")
    build_status = str(setup_response["status"])

    if build_status == "pending":
        upload_cortex_files(
            upload_url=setup_response["uploadUrl"],
            zip_file_name=os.path.basename(setup_response["keyName"]),
            config=config,
            file_list=file_list,
            disable_animation=disable_animation,
        )

    build_status = _poll_logs(
        build_id=build_id,
        cerebrium_config=config,
        build_status=build_status,
        disable_animation=disable_animation,
    )

    return build_status, setup_response


def _poll_logs(
    build_id: str,
    cerebrium_config: CerebriumConfig,
    build_status: str,
    disable_animation: bool = False,
) -> str:
    spinner = None
    if build_status == "pending":
        spinner = (
            None if disable_animation else Spinner("dots", "Building App...", style="gray")
        )

        live = Live(spinner, console=console, refresh_per_second=10)

        # Start the Live context using the start() method
        live.start()
        try:
            build_status = poll_build_logs(build_id, cerebrium_config.deployment.name, 1)

        except KeyboardInterrupt:
            # If user presses Ctrl-C, signal all threads to stop
            live.stop()
            _graceful_shutdown(
                app_name=cerebrium_config.deployment.name,
                build_id=build_id,
                is_interrupt=True,
            )
        finally:
            # Stop the Live instance after the loop
            live.stop()
    elif build_status == "running":
        print("🤷 No file changes detected. Not fetching logs")
    else:
        if spinner:
            spinner.stop(text="Build failed")
        cerebrium_log("ERROR", "Build failed.")

    return build_status
