import subprocess
from pathlib import Path
from shutil import which
from .exceptions import DependencyMissingError


class Applier:
    def __init__(self, config):
        self.config = config

    def _get_wallpaper_cmd(self) -> str:
        user_choice = self.config.wallpaper_daemon
        if user_choice != "auto":
            if which(user_choice):
                return user_choice
            raise DependencyMissingError(
                f"{user_choice} not found on your system."
            )

        for d in ["awww", "swww", "hyprpaper"]:
            if which(d):
                return d
        raise DependencyMissingError(
                "No wallpaper daemon was found on your system."
            )

    def apply_wallpaper(self, path: Path | str) -> None:
        wall_daemon = self._get_wallpaper_cmd()
        if wall_daemon == "hyprpaper":
            subprocess.run(
                ["hyprctl", wall_daemon, "preload", f"{path}"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True)

            subprocess.run(
                ["hyprctl", wall_daemon, "wallpaper", f",{path}"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True)
            return
        else:
            subprocess.run(
                [wall_daemon, "img", str(path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True)

    def apply_pywal(self, path: Path | str) -> None:
        if not which("wal"):
            raise DependencyMissingError("pywal not found on your system.")
        subprocess.run(
            ["wal", "-i", str(path), "-n"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True)

    def reload_waybar(self) -> None:
        subprocess.run(
            ["killall", "-SIGUSR2", "waybar"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False)

    def apply_all(self, path: Path | str):
        self.apply_wallpaper(path)
        self.apply_pywal(path)
        self.reload_waybar()
