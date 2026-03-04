import typer
from rich.console import Console
from typing import Annotated
from .controller import Controller
from .config import ConfigManager, ConfigEnum
from .utils import handle_errors
from .utils import sexy_terminal_theme

console = Console(theme=sexy_terminal_theme, color_system="truecolor")
config_app = typer.Typer(
    help="Provides commands for managing configuration."
)


@config_app.command(
    "set",
    help="Update a specific configuration setting."
)
@handle_errors
def set_config(
    attr: Annotated[
        ConfigEnum, typer.Argument(
            help="The configuration attribute to modify(e.g. mode, pywal).")
    ],
    val: Annotated[
        str, typer.Argument(help="The new value to assign to the attribute.")
        ]
) -> None:
    controller = Controller()
    controller.update_config(**{attr.value: val})
    console.print(
        f"[bold][green_dk]Successfuly updated [/][cyan_br]{attr.value}[/].")


@config_app.command(
    "reset",
    help="Resets the configuration file to default values."
)
@handle_errors
def reset() -> None:
    reset_everything = typer.confirm(
        "Are you sure you want to reset your configuration?",
        default=False
    )
    if not reset_everything:
        console.print("[yellow_br]Reset cancelled.[/]")
        raise typer.Abort()
    config = ConfigManager(load=False)
    config.reset()
    console.print("[bold][green_dk]Configuration has been "
                  "reset to defaults[/][/]")


if __name__ == "__main__":
    config_app()
