import re
from collections.abc import Iterable

from rich.console import Console
from rich.logging import RichHandler
from termcolor import colored
from termcolor._types import Color, Attribute
from yaspin.core import Yaspin

import logging
from cerebrium.types import LogLevel

logger = logging.getLogger("rich")

# Create a console object
console = Console(highlight=False)

__LOG_DEBUG_DELIMITERS__ = ["|| DEBUG ||", "|| END DEBUG ||"]
__LOG_INFO_DELIMITERS__ = ["|| INFO ||", "|| END INFO ||"]
__LOG_ERROR_DELIMITERS__ = ["|| ERROR ||", "|| END ERROR ||"]

__re_debug__ = re.compile(r"^\|\| DEBUG \|\| (.*) \|\| END DEBUG \|\|")
__re_info__ = re.compile(r"^\|\| INFO \|\| (.*) \|\| END INFO \|\|")
__re_error__ = re.compile(r"^\|\| ERROR \|\| (.*) \|\| END ERROR \|\|")

rich_handler = RichHandler(
    console=console,
    rich_tracebacks=False,
    show_path=False,
    show_level=False,
    show_time=False,
    markup=True,
    highlighter=None,  # Explicitly disable syntax highlighting for log messages
)
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S.%f",  # Include timestamp with milliseconds
    handlers=[rich_handler],
)


def get_logger():
    global logger
    global rich_handler

    if logger is None:
        # re-initialise if the task is different
        rich_handler = RichHandler(
            console=console,
            rich_tracebacks=False,
            show_path=False,
            show_level=False,
            show_time=True,
            markup=True,
            highlighter=None,  # Explicitly disable syntax highlighting for log messages
        )
        # Setup logging globally

    return logger


error_messages = {
    "disk quota exceeded": "💾 You've run out of space in your /persistent-storage. \n"
    "You can add more by running the command: `cerebrium storage increase-capacity <the_amount_in_GB>`"
}  # Error messages to check for


def cerebrium_log(
    message: str,
    prefix: str = "",
    level: LogLevel = "INFO",
    attrs: Iterable[Attribute] = [],
    color: Color = "cyan",
    prefix_seperator: str = "\t",
    spinner: Yaspin | None = None,
):
    """User-friendly coloured logging

    Args:
        message (str): Error message to be displayed
        prefix (str): Prefix to be displayed. Defaults to empty.
        level (str): Log level. Defaults to "INFO".
        attrs (list, optional): Attributes for colored printing. Defaults to None.
        color (str, optional): Color to print in. Defaults depending on log level.
        prefix_seperator (str, optional): Seperator between prefix and message. Defaults to "\t".
        spinner (Yaspin, optional): Spinner object to write to. Defaults to None.
    """
    log_level = level.upper()
    default_prefixes = {
        "DEBUG": "Debug",
        "INFO": "Info: ",
        "WARNING": "Warning: ",
        "ERROR": "Error: ",
    }
    default_colors: dict[str, Color] = {
        "DEBUG": "grey",
        "INFO": "cyan",
        "WARNING": "yellow",
        "ERROR": "red",
    }
    prefix = prefix or default_prefixes.get(log_level, "")

    # None is default for unused variables to avoid breaking termcolor
    log_color = default_colors.get(level, "cyan")
    prefix = colored(f"{prefix}", color=log_color, attrs=["bold"])
    message = colored(f"{message}", color=log_color, attrs=attrs)

    # spinners don't print nicely and keep spinning on errors. Use them if they're there
    if spinner:
        spinner.write(prefix)  # type: ignore
        spinner.text = ""
        if level == "ERROR":
            spinner.fail(message)
            spinner.stop()
        else:
            spinner.write(message)  # type: ignore
    else:
        print(prefix, end=prefix_seperator)
        print(message)
