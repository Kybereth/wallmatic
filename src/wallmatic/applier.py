import subprocess
from pathlib import Path
from shutil import which
from abc import ABC, abstractmethod
from .exceptions import DependencyMissingError, ConfigError


class WallpaperEngine(ABC):
    @abstractmethod
    def is_installed(self) -> bool:
        pass

    @abstractmethod
    def apply(self, path: Path) -> None:
        pass


class ColorEngine(ABC):
    @abstractmethod
    def is_installed(self) -> bool:
        pass

    @abstractmethod
    def apply(self, path: Path) -> None:
        pass


class HyprpaperEngine(WallpaperEngine):
    def is_installed(self) -> bool:
        return bool(which("hyprctl"))

    def apply(self, path: Path):
        subprocess.run(
            ["hyprctl", "hyprpaper", "preload", f"{path}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True)

        subprocess.run(
            ["hyprctl", "hyprpaper", "wallpaper", f",{path}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True)


class AwwwEngine(WallpaperEngine):
    def __init__(self) -> None:
        self._cmd: str | None = None

    def is_installed(self) -> bool:
        if which("awww"):
            self._cmd = "awww"
            return True
        elif which("swww"):
            self._cmd = "swww"
            return True
        return False

    def apply(self, path: Path):
        if not (self._cmd or self.is_installed()):
            raise DependencyMissingError("Neither 'awww' nor 'swww' was found")
        subprocess.run(
            [self._cmd, "img", str(path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True)


class PywalEngine(ColorEngine):
    def is_installed(self):
        return bool(which("wal"))

    def apply(self, path: Path):
        subprocess.run(
            ["wal", "-i", str(path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )


class WallustEngine(ColorEngine):
    def is_installed(self):
        return bool(which("wallust"))

    def apply(self, path: Path):
        subprocess.run(
            ["wallust", "run", str(path), "-n"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True)


class NoColorEngine(ColorEngine):
    def is_installed(self) -> bool:
        return True

    def apply(self, path: Path) -> None:
        pass


class WallpaperEngineFactory:
    _ENGINES = {
        "swww": AwwwEngine,
        "awww": AwwwEngine,
        "hyprpaper": HyprpaperEngine,
    }

    @classmethod
    def create(cls, daemon_name: str) -> WallpaperEngine:
        daemon_name = daemon_name.lower()
        engine_instance: WallpaperEngine

        if daemon_name == "auto":
            for engine_class in cls._ENGINES.values():
                engine_instance = engine_class()
                if engine_instance.is_installed():
                    return engine_instance
            raise DependencyMissingError(
                f"No wallpaper daemon ({'/'.join(cls._ENGINES)})"
                " was found on your system."
            )
        if daemon_name not in cls._ENGINES:
            raise ConfigError(f"Unknown wallpaper daemon: '{daemon_name}'")

        engine_instance = cls._ENGINES[daemon_name]()
        if not engine_instance.is_installed():
            raise DependencyMissingError(
                f"{daemon_name} is configured,"
                "but it's not found on your system."
            )

        return engine_instance


class ColorEngineFactory:
    _ENGINES = {
        "pywal": PywalEngine,
        "wallust": WallustEngine,
        "none": NoColorEngine
    }

    @classmethod
    def create(cls, engine_name: str) -> ColorEngine:
        engine_name = engine_name.lower()

        if engine_name not in cls._ENGINES:
            raise ConfigError(f"Unknown color engine: '{engine_name}'")

        engine_instance = cls._ENGINES[engine_name]()
        if not engine_instance.is_installed():
            raise DependencyMissingError(f"{engine_name} is configured,"
                                         " but it's not found on your system")
        return engine_instance


class Applier:
    def __init__(self, config):
        self.config = config

    def reload_waybar(self) -> None:
        subprocess.run(
            ["killall", "-SIGUSR2", "waybar"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False)

    def apply_all(self, path: Path | str) -> None:
        path = Path(path)

        wallpaper_engine = WallpaperEngineFactory.create(
            self.config.wallpaper_daemon)
        color_engine = ColorEngineFactory.create(self.config.color_engine)

        wallpaper_engine.apply(path)
        color_engine.apply(path)
        self.reload_waybar()
