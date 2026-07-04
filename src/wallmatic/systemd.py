import shutil
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
Description=Wallmatic Wallpaper Changer Service
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

    def generate_timer(self, trigger_type: str, value: str) -> str:
        if trigger_type == "interval":
            line = f"OnUnitActiveSec={value}"
        elif trigger_type == "calendar":
            line = f"OnCalendar=*-*-* {value}"
        else:
            raise ValueError(f"Unknow trigger type: {trigger_type}")
        return self.TIMER_TEMPLATE.format(trigger_line=line)

    def generate_service(self, restore: bool = False) -> str:
        if restore:
            return self.RESTORE_SERVICE_TEMPLATE.format(exec_path=self._get_exec_path())
        return self.SERVICE_TEMPLATE.format(exec_path=self._get_exec_path())
