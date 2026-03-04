import typer
from pathlib import Path
from functools import wraps
from typing import Callable, Any
from rich.console import Console
from rich.theme import Theme
from subprocess import CalledProcessError
from .exceptions import NoValidImagesFoundError
from .exceptions import DirectoryNotFoundError
from .exceptions import ThemeNotSetError
from .exceptions import ConfigError
from .exceptions import DependencyMissingError

sexy_terminal_theme = Theme({
    "black_dk": "#282a2e",
    "black_br": "#373b41",
    "red_dk": "#a54242",
    "red_br": "#cc6666",
    "green_dk": "#8c9440",
    "green_br": "#b5bd68",
    "yellow_dk": "#de935f",
    "yellow_br": "#f0c674",
    "blue_dk": "#5f819d",
    "blue_br": "#81a2be",
    "magenta_dk": "#85678f",
    "magenta_br": "#b294bb",
    "cyan_dk": "#5e8d87",
    "cyan_br": "#8abeb7",
    "white_dk": "#707880",
    "white_br": "#c5c8c6"
})


def handle_errors(func: Callable[..., Any]) -> Callable[..., Any]:
    console = Console(theme=sexy_terminal_theme, color_system="truecolor")

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except (NoValidImagesFoundError,
                DirectoryNotFoundError,
                ThemeNotSetError,
                ) as e:
            console.print(
                f"[bold][red_dk]Error: [/][/][red_br]{e}[/]")
            raise typer.Exit(code=1)
        except ConfigError as e:
            console.print(
                "[bold][red_dk]Configuration error: [/][/]"
                f"[red_br]{e}[/]")
            console.print(
                "[bold][magenta_dk]Hint: [/][/]"
                "[magenta_br]Check or reset your configuration.[/]"
            )
            raise typer.Exit(code=1)
        except FileNotFoundError as e:
            console.print("[bold][red_dk]Error: [/][/]"
                          f"[red_br]File not found {e.filename}[/]")
            raise typer.Exit(code=1)
        except DependencyMissingError as e:
            console.print("[bold][red_dk]Error: [/][/]"
                          f"[red_br]{e}[/]")
            console.print(
                "[bold][magenta_dk]Hint: [/][/]"
                "[magenta_br]Check if you have installed "
                "the required packages.[/]"
                          )
            raise typer.Exit(code=1)
        except CalledProcessError as e:
            console.print("[bold][red_dk]Error: [/][/] "
                          "[red_br]Command failed "
                          f"with exit code {e.returncode}.[/]"
                          )
            raise typer.Exit(code=1)
    return wrapper


def path_collapse_user(path: str | Path) -> str:
    if not isinstance(path, (str, Path)):
        raise TypeError(
            "Expected type str or pathlib.Path, "
            f"but got {type(path).__name__}."
        )
    home_path = str(Path.home())
    str_path = str(path)
    if str_path.startswith(home_path):
        return str_path.replace(home_path, "~", 1)
    return str_path
