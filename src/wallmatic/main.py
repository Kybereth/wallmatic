import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import Annotated
from pathlib import Path
from enum import Enum
from wallmatic.controller import Controller
from wallmatic.config import ConfigManager
from wallmatic.config_cli import config_app
from wallmatic.utils import handle_errors
from wallmatic.utils import path_collapse_user
from wallmatic.utils import sexy_terminal_theme


console = Console(theme=sexy_terminal_theme, color_system="truecolor")

app = typer.Typer(
    rich_markup_mode="rich")
app.add_typer(config_app, name="config")


class Mode(str, Enum):
    glob = "global"
    mood = "mood"
    static = "static"


def show_logo():
    ascii_logo = (r"""
 __        __    _ _                 _   _
 \ \      / /_ _| | |_ __ ___   __ _| |_(_) ___
  \ \ /\ / / _` | | | '_ ` _ \ / _` | __| |/ __|
   \ V  V / (_| | | | | | | | | (_| | |_| | (__
    \_/\_/ \__,_|_|_|_| |_| |_|\__,_|\__|_|\___|""")
    console.print(Panel(ascii_logo, style="blue_br", expand=False))


@app.command(
    "init",
    help="Setup Wallmatic: create config and set the wallpapers directory."
)
@handle_errors
def init(directory: Annotated[
        Path, typer.Option(
            "--directory",
            "-d",
            help="Directory where you store the wallpapers")
        ]) -> None:
    show_logo()
    config = ConfigManager()
    config.wallpapers_dir = directory
    config.save()

    console.print("[bold][green_dk]Wallmatic initialized![/][/]")
    console.print("[dim][green_br]Wallpapers directory set to [/][/]"
                  f"[dim][cyan_br]{directory}[/][/]")


@app.command(
    "status",
    help="Shows the most important settings from the config."
)
@handle_errors
def status() -> None:
    config: ConfigManager = ConfigManager()

    table = Table(title="Wallmatic status",
                  title_style="#8c9440",
                  header_style="#f0c674",
                  border_style="#c5c8c6")
    table.add_column("Property", style="#b294bb")
    table.add_column("Value", style="#81a2be")

    pywal_status = "Enabled" if config.pywal else "Disabled"
    theme_status = config.theme if config.theme else "Not set"

    if config.current_image:
        wallpaper_status = path_collapse_user(config.current_image)
    else:
        wallpaper_status = "Not set"

    table.add_row("Wallpaper", wallpaper_status)
    table.add_row("Mode", config.mode)
    table.add_row("Theme", theme_status)
    table.add_row("Pywal integration", pywal_status)
    table.add_row("Wallpaper directory",
                  path_collapse_user(config.wallpapers_dir)
                  )
    console.print(table)


@app.command(
    "show-themes",
    help="Displays a list of themes."
)
@handle_errors
def show_themes() -> None:
    controller = Controller()
    themes = controller.selector.list_themes()
    if not themes:
        console.print("[bold][yellow_dk]No themes found[/][/]")
        console.print(
            "[dim][maganeta_dk]Hint:[/][/] "
            "[dim][maganeta_br]Ensure wallpaper directories"
            "exists or verify the main"
            "wallpaper directory in config[/][/]")
        return
    console.print("[bold][green_dk]Available themes:[/][/]")
    themes.sort()
    for i, t in enumerate(themes):
        console.print(f"[cyan_br]  {i} {t}[/]")


@app.command(
    "next",
    help="Selects the next wallpaper depending on your current mode."
)
@handle_errors
def next_wallpaper() -> None:
    controller = Controller()
    console.print(
        "[dim][green_dk]Current mode: [/]"
        f"[cyan_br]{controller.config.mode}[/][/]")

    with console.status(
        "[bold][cyan_dk]Searching for and applying "
        "new wallpaper[/][/]..."
    ):
        wallpaper_path = controller.next()
    collapsed_wal = path_collapse_user(wallpaper_path)
    console.print("[bold][green_dk]Applied new wallpaper: [/][/]"
                  f"[cyan_br]{collapsed_wal}[/]")


@app.command(
    "restore",
    help="Restores the last appearance from the config."
)
@handle_errors
def restore() -> None:
    controller = Controller()

    with console.status("[bold][cyan_dk]Restoring and applying "
                        "previous wallpaper[/][/]..."):
        controller.restore()
    collapsed_wal = path_collapse_user(controller.config.current_image)
    console.print(
        "[bold][green_dk]Successfully restored wallpaper: [/][/]"
        f"[cyan_br]{collapsed_wal}[/]")


@app.command(
    "set-mode",
    help=(
        "Set the wallpaper change mode.\n\n"
        "MODES:\n"
        " * [bold]global[/bold]: Pick a random image from any theme.\n"
        " * [bold]mood[/bold]:   Pick a random image from a specific theme.\n"
        " * [bold]static[/bold]: Set a specific image by its path."
         )
)
@handle_errors
def set_mode(
    mode: Annotated[
        Mode, typer.Argument(help="Wallpaper change mode to use.")
    ] = Mode.glob,
    theme: Annotated[
        str, typer.Option("--theme", "-t", help="Theme name to pick from.")
    ] = None,
    image: Annotated[
        str, typer.Option("--image", "-i", help="Path to a specific image.")
    ] = None
) -> None:
    controller = Controller()
    with console.status(
        "[bold][cyan_dk]Changing mode and performing "
        "required tasks...[/][/]"
    ):
        controller.set_mode(mode.value, theme, image)
    console.print("[bold][green_dk]Mode changed to [/][/]"
                  f"[cyan_br]{mode.value}[/]")
    if mode == Mode.mood and theme:
        console.print(
            "[dim][green_dk]    Theme: [/][/]"
            f"[dim][cyan_br]{theme}[/][/]")
    console.print("[dim][green_dk]    Applied wallpaper: [/][/]"
                  f"[dim][cyan_br]{controller.config.current_image}[/][/]")


def main():
    app(prog_name="Wallmatic")


if __name__ == "__main__":
    main()
