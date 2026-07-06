import typer
import subprocess
from rich.console import Console
from typing import Annotated
from .utils import handle_errors, sexy_terminal_theme
from .controller import Controller

console = Console(theme=sexy_terminal_theme, color_system="truecolor")
timer_app = typer.Typer(
    help="Manage automated wallpaper switching."
)


@timer_app.command(
    "enable",
    help="Enable automated wallpaper switching using systemd."
)
@handle_errors
def enable(
    interval: Annotated[
        str, typer.Option(
            "--interval",
            "-i",
            help="The time interval between changes. "
                 "Format: digits + s/m/h/d (e.g., 15m, 2h)."
        )
    ] = None,
    hours: Annotated[
        str, typer.Option(
            "--hours",
            "-h",
            help="Systemd OnCalendar execution "
                 "hours (e.g., 21:00 or 09,18:00)."
        )
    ] = None,
    restore: Annotated[
        bool, typer.Option(
            "--restore/--no-restore",
            "-r/-nr",
            help="Restore the previous wallpaper on session startup."
        )
    ] = False,
    boot: Annotated[
        bool, typer.Option(
            "--change-on-boot/--no-change-on-boot",
            "-c/-nc",
            help="Apply a new random wallpaper on session startup."
        )
    ] = False,
):
    if (interval is None) == (hours is None):
        console.print("[bold][red_dk]Error:[/][/] Provide either "
                      "--interval or --hours (not both or neither)")
        raise typer.Exit(code=1)
    elif restore and boot:
        console.print("[bold][red_dk]Error:[/][/] --restore and "
                      "--change-on-boot cannot be used together")
        raise typer.Exit(code=1)

    if interval is not None:
        trigger_type = "interval"
        val = interval
    elif hours is not None:
        trigger_type = "calendar"
        val = hours

    controller = Controller()
    controller.enable_automation(
        trigger_type,
        val,
        restore,
        boot
    )


@timer_app.command(
    "disable",
    help="Disable automated wallpaper switching using systemd."
)
@handle_errors
def disable():
    controller = Controller()
    controller.disable_automation()


@timer_app.command(
    "status",
    help="Show the current automation status from systemd."
)
@handle_errors
def status():
    controller = Controller()
    state = controller.config.automation

    if not state["enabled"]:
        console.print("[bold][yellow_dk]Automation is disabled "
                      "in config.[/][/]")
        return

    res = subprocess.run(
        ["systemctl", "--user", "is-active", "wallmatic.timer"],
        capture_output=True,
        text=True
    )

    systemd_status = res.stdout.strip()

    console.print("[bold][green_dk]Automation: [/][/][green_br]Enabled[/]")
    console.print(
        f"    [magenta_br]Trigger Type:[/] {state['trigger_type']}"
    )
    console.print(
        "    [magenta_br]Value:[/] "
        f"{state['interval_value'] or state['calendar_value']}"
    )
    console.print(
        "    [magenta_br]Systemd Timer[/] "
        f"[cyan_br]{systemd_status}[/]"
    )
