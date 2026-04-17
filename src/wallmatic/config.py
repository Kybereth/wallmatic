import yaml
import pathlib
from typing import Any
from copy import deepcopy
from .exceptions import ConfigError
from enum import Enum


class ConfigEnum(str, Enum):
    wallpapers_dir = "wallpapers_dir"
    mode = "mode"
    theme = "theme"
    previous_image = "previous_image"
    current_image = "current_image"
    pywal = "pywal"
    auto = "auto"
    wallpaper_daemon = "wallpaper_daemon"


class ConfigManager:
    APP_NAME = "wallmatic"

    STD_WALL_DIR = pathlib.Path.home() / "Pictures" / "Wallpapers"

    CONFIG_DIR = pathlib.Path.home() / ".config" / APP_NAME

    CONFIG_FILE = pathlib.Path.home() / ".config" / APP_NAME / "config.yaml"

    STD_CONFIG = {
        "wallpapers_dir": str(STD_WALL_DIR),
        "mode": "global",
        "theme": None,
        "previous_image": None,
        "current_image": None,
        "pywal": False,
        "auto": False,
        "wallpaper_daemon": "auto"
    }

    PATH_KEYS = {"wallpapers_dir", "previous_image", "current_image"}
    BOOL_KEYS = {"pywal", "auto"}
    OTHER_KEYS = {"mode", "theme", "wallpaper_daemon"}

    def __init__(
        self,
        config_file: pathlib.Path | None = None,
        load: bool = True
    ):
        self._wallpapers_dir: pathlib.Path | None = None
        self._current_image: pathlib.Path | None = None
        self._previous_image: pathlib.Path | None = None

        self._mode: str | None = None
        self._theme: str | None = None
        self._wallpaper_daemon: str | None = None

        self._pywal: bool = False
        self._auto: bool = False

        if config_file:
            self._config_file = config_file
            self._config_dir = self._config_file.parent
        else:
            self._config_file = self.CONFIG_FILE
            self._config_dir = self.CONFIG_DIR

        self._config = deepcopy(self.STD_CONFIG)
        if load and self.is_conf_file():
            self._config.update(self.from_file())
        self.from_dict()

    def is_conf_dir(self):
        return self._config_dir.is_dir()

    def is_conf_file(self):
        return self._config_file.is_file()

    @classmethod
    def parse_value(
        cls,
        key: str,
        val: Any
    ) -> pathlib.Path | str | bool | None:
        if val is None:
            return None
        elif key in cls.PATH_KEYS:
            return pathlib.Path(val).expanduser().resolve()
        elif key in cls.BOOL_KEYS:
            normalized_val = str(val).lower()
            if normalized_val in ("true", "t", "yes", "on", "1"):
                return True
            elif normalized_val in ("false", "f", "no", "off", "0"):
                return False
        return val

    def to_dict(self) -> dict[str, Any]:
        conf = {
            "wallpapers_dir": (
                str(self._wallpapers_dir)
                if self._wallpapers_dir
                else None
            ),
            "mode": self._mode,
            "theme": self._theme,
            "previous_image": (
                str(self._previous_image)
                if self._previous_image
                else None
            ),
            "current_image": (
                str(self._current_image)
                if self._current_image
                else None),
            "pywal": self._pywal,
            "auto": self._auto,
            "wallpaper_daemon": self._wallpaper_daemon
        }
        return conf

    def from_file(self) -> dict[str, Any]:
        try:
            with open(str(self._config_file), "r") as conff:
                data = yaml.safe_load(conff) or {}
                return data
        except (yaml.YAMLError, OSError) as e:
            raise ConfigError(
                f"The configuration file is corrupted or unreadable: {e}")

    def save(self) -> None:
        self._config_dir.mkdir(parents=True, exist_ok=True)
        tmp_path = self._config_file.with_suffix(".tmp")
        with open(tmp_path, "w") as conff:
            yaml.safe_dump(self.to_dict(), conff)
        tmp_path.replace(self._config_file)

    def reset(self) -> None:
        self._config = deepcopy(self.STD_CONFIG)
        self.from_dict()
        self.save()

    def from_dict(self) -> None:
        for key, val in self._config.items():
            if key in (self.PATH_KEYS | self.BOOL_KEYS | self.OTHER_KEYS):
                parsed_val = self.parse_value(key, val)
                setattr(self, key, parsed_val)

    @property
    def wallpapers_dir(self) -> pathlib.Path:
        return self._wallpapers_dir

    @wallpapers_dir.setter
    def wallpapers_dir(self, val: pathlib.Path | str | None) -> None:
        try:
            if val is None:
                dir_path = self.STD_WALL_DIR
            else:
                dir_path = pathlib.Path(val).expanduser().absolute()

            dir_path.mkdir(parents=True, exist_ok=True)

            if not dir_path.is_dir():
                raise ConfigError(
                    f"Failed to create or find directory: {dir_path}")
            self._wallpapers_dir = dir_path
        except (ValueError, TypeError, OSError) as e:
            raise ConfigError(f"Invalid path: {e}")

    @property
    def mode(self) -> str:
        return self._mode

    @mode.setter
    def mode(self, val: str | Enum) -> None:
        val = val.value if isinstance(val, Enum) else val
        if val in {"global", "mood", "static"}:
            self._mode = val
        else:
            raise ConfigError("Invalid value: mode has to be "
                              "'global', 'mood' or 'static'")

    @property
    def theme(self) -> str:
        return self._theme

    @theme.setter
    def theme(self, val: str | None) -> None:
        if isinstance(val, (str, type(None))):
            self._theme = val
        else:
            raise ConfigError(
                f"Invalid value type {type(val).__name__}: theme has to be str"
            )

    @property
    def previous_image(self) -> pathlib.Path:
        return self._previous_image

    @previous_image.setter
    def previous_image(self, val: pathlib.Path | None) -> None:
        try:
            self._previous_image = (
                pathlib.Path(val).expanduser().resolve()
                if val else None
            )
        except (ValueError, TypeError):
            raise ConfigError("Invalid path")

    @property
    def current_image(self) -> pathlib.Path:
        return self._current_image

    @current_image.setter
    def current_image(self, val: pathlib.Path | str) -> None:
        try:
            self._current_image = (
                pathlib.Path(val).expanduser().resolve()
                if val else None
            )
        except (ValueError, TypeError):
            raise ConfigError("Invalid Path")

    @property
    def pywal(self) -> bool:
        return self._pywal

    @pywal.setter
    def pywal(self, val: bool) -> None:
        if isinstance(val, bool):
            self._pywal = val
        else:
            raise ConfigError(
                (f"Invalid value type {type(val).__name__}: "
                 "pywal has to be bool")
            )

    @property
    def auto(self) -> bool:
        return self._auto

    @auto.setter
    def auto(self, val: bool) -> None:
        if isinstance(val, bool):
            self._auto = val
        else:
            raise ConfigError(
                f"Invalid value type {type(val).__name__}: auto has to be bool"
            )

    @property
    def wallpaper_daemon(self) -> str:
        return self._wallpaper_daemon

    @wallpaper_daemon.setter
    def wallpaper_daemon(self, val: str) -> None:
        if isinstance(val, str):
            self._wallpaper_daemon = val
        else:
            raise ConfigError(
                f"Invalid value type {type(val).__name__}: "
                "wallpaper_daemon has to be str"
            )
