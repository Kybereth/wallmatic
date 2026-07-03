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
    def apply(self, path: Path, options: dict | None = None) -> None:
        pass

    @property
    @abstractmethod
    def supported_formats(self) -> set[str]:
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

    @property
    def supported_formats(self) -> set[str]:
        return {".jpg", ".jpeg", ".png", ".webp"}

    def apply(self, path: Path, options: dict | None = None):
        subprocess.run(
            ["hyprctl", "hyprpaper", "preload", f"{path}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            check=True)

        subprocess.run(
            ["hyprctl", "hyprpaper", "wallpaper", f",{path}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
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

    @property
    def supported_formats(self) -> set[str]:
        return {".jpg", ".jpeg", ".png", ".webp", ".gif",
                ".bmp", ".pnm", ".tga", ".tiff"}

    def apply(self, path: Path, options: dict | None = None):
        if not (self._cmd or self.is_installed()):
            raise DependencyMissingError("Neither 'awww' nor 'swww' was found")

        cmd = [self._cmd, "img", str(path)]

        if options:
            for key, val in options.items():
                if val is not None and val != "":
                    cmd.extend([f"--{key}", str(val)])

        subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            check=True)


class PywalEngine(ColorEngine):
    def is_installed(self):
        return bool(which("wal"))

    def apply(self, path: Path):
        subprocess.run(
            ["wal", "-i", str(path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )


class WallustEngine(ColorEngine):
    def is_installed(self):
        return bool(which("wallust"))

    def apply(self, path: Path):
        subprocess.run(
            ["wallust", "run", str(path), "-n"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
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
    def __init__(self, config, wallpaper_engine, color_engine):
        self.config = config
        self.wallpaper_engine = wallpaper_engine
        self.color_engine = color_engine

    def reload_waybar(self) -> None:
        subprocess.run(
            ["killall", "-SIGUSR2", "waybar"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            check=False)

    def apply_all(self, path: Path | str) -> None:
        path = Path(path)

        opts = self.config.daemon_options.get(
            self.config.wallpaper_daemon, {}
        )

        self.wallpaper_engine.apply(path, options=opts)
        self.color_engine.apply(path)
        self.reload_waybar()
