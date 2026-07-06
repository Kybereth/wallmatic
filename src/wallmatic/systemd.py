import shutil
import subprocess
from pathlib import Path


class SystemdManager:
    USER_SYSTEMD_DIR = Path("~/.config/systemd/user/").expanduser()

    SERVICE_TEMPLATE = """[Unit]
Description=Wallmatic Wallpaper Changer Service
After=graphical-session.target

[Service]
Type=oneshot
ExecStart={exec_path} next
    """

    RESTORE_SERVICE_TEMPLATE = """[Unit]
Description=Wallmatic Wallpaper Restore Service
After=graphical-session.target

[Service]
Type=oneshot
ExecStart={exec_path} restore
    """

    TIMER_TEMPLATE = """[Unit]
Description=Wallmatic Wallpaper Changer Timer

[Timer]
{trigger_line}
Persistent=true

[Install]
WantedBy=timers.target
    """

    def _get_exec_path(self) -> str:
        return shutil.which("wallmatic")

    def generate_timer(self,
                       trigger_type: str,
                       value: str,
                       change_on_boot: bool = False
                       ) -> str:
        lines = []
        if trigger_type == "interval":
            lines.append("OnActiveSec=1s")
            lines.append(f"OnUnitActiveSec={value}")
        elif trigger_type == "calendar":
            lines.append(f"OnCalendar=*-*-* {value}")
        else:
            raise ValueError(f"Unknown trigger type: {trigger_type}")

        if change_on_boot:
            lines.append("OnStartupSec=10s")

        trigger_line = "\n".join(lines)
        return self.TIMER_TEMPLATE.format(trigger_line=trigger_line)

    def generate_service(self, restore: bool = False) -> str:
        if restore:
            return self.RESTORE_SERVICE_TEMPLATE.format(
                exec_path=self._get_exec_path()
            )
        return self.SERVICE_TEMPLATE.format(exec_path=self._get_exec_path())

    def write_unit_files(self, automation_data: dict) -> None:
        self.USER_SYSTEMD_DIR.mkdir(parents=True, exist_ok=True)

        if automation_data["trigger_type"] == "interval":
            time_val = automation_data["interval_value"]
        else:
            time_val = automation_data["calendar_value"]

        base_service = self.generate_service(restore=False)
        (self.USER_SYSTEMD_DIR / "wallmatic.service").write_text(base_service)

        timer_text = self.generate_timer(
            automation_data["trigger_type"],
            time_val,
            automation_data["change_on_boot"]
        )
        (self.USER_SYSTEMD_DIR / "wallmatic.timer").write_text(timer_text)

        restore_path = self.USER_SYSTEMD_DIR / "wallmatic-restore.service"
        if automation_data["restore_on_boot"]:
            restore_service = self.generate_service(restore=True)
            restore_path.write_text(restore_service)
        else:
            restore_path.unlink(missing_ok=True)

    def clear_unit_files(self) -> None:
        for unit in ["wallmatic.service",
                     "wallmatic.timer",
                     "wallmatic-restore.service"]:
            (self.USER_SYSTEMD_DIR / unit).unlink(missing_ok=True)

    def start(self, restore_on_boot: bool) -> None:
        subprocess.run(
            ["systemctl", "--user", "daemon-reload"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        subprocess.run(
            ["systemctl", "--user", "enable", "--now", "wallmatic.timer"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        if restore_on_boot:
            subprocess.run(
                ["systemctl", "--user", "enable", "wallmatic-restore.service"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )

    def stop(self) -> None:
        subprocess.run(
            ["systemctl", "--user", "disable", "--now", "wallmatic.timer"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        if (self.USER_SYSTEMD_DIR / "wallmatic-restore.service").exists():
            subprocess.run(
                [
                    "systemctl",
                    "--user",
                    "disable",
                    "wallmatic-restore.service"
                 ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
        subprocess.run(
            ["systemctl", "--user", "daemon-reload"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
