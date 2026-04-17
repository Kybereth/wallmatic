from pathlib import Path
from .config import ConfigManager
from .selector import Selector
from .applier import Applier
from .exceptions import NoValidImagesFoundError
from .exceptions import ThemeNotSetError


class Controller:
    def __init__(self):
        self.config = ConfigManager()
        self.selector = Selector(self.config)
        self.applier = Applier(self.config)

    def _update_and_apply(self, wallpaper: str | Path) -> None:
        self.config.previous_image = self.config.current_image
        self.config.current_image = wallpaper

        if self.config.pywal:
            self.applier.apply_pywal(wallpaper)
        self.applier.apply_wallpaper(wallpaper)
        self.applier.reload_waybar()

        self.config.save()

    def update_config(self, **kwargs) -> None:
        for key, val in kwargs.items():
            if (
                hasattr(self.config, key)
                and
                not key.startswith("_")
                and
                not key.startswith("__")
            ):
                parsed_val = self.config.parse_value(key, val)
                setattr(self.config, key, parsed_val)

            else:
                raise AttributeError(
                    f"The attribute {key} doesn't exist in config"
                )
        self.config.save()

    def reset_config(self):
        self.config.reset()

    def restore(self) -> None:
        wallpaper = self.config.current_image
        if not wallpaper:
            raise NoValidImagesFoundError(
                "No current image found. Try using set-mode")
        self._update_and_apply(wallpaper)

    def set_mode(
        self,
        mode: str,
        theme: str | None = None,
        image: str | None = None
    ) -> None:
        if mode == "global":
            wallpaper = self.selector.rand_glob_wallpaper()
            self._update_and_apply(wallpaper)
            self.config.mode = mode

        elif mode == "mood":
            target_theme = theme or self.config.theme
            if target_theme in (None, ""):
                raise ThemeNotSetError("Theme must be specified for mood mode")

            wallpaper = self.selector.rand_mood_wallpaper(target_theme)

            self.config.theme = target_theme
            self.config.mode = mode
            self._update_and_apply(wallpaper)

        elif mode == "static":
            wallpaper = image or (self.config.current_image
                                  or self.config.previous_image)
            if wallpaper in (None, ""):
                raise NoValidImagesFoundError(
                    "No image specified and no current image found in config"
                )
            path_img = Path(wallpaper).expanduser().resolve()
            if not path_img.exists():
                raise NoValidImagesFoundError(f"Image not found: {path_img}")
            self.config.mode = mode
            self._update_and_apply(path_img)

    def next(self) -> str:
        if self.config.mode == "global":
            wallpaper = self.selector.rand_glob_wallpaper()
            self._update_and_apply(wallpaper)
            return wallpaper

        elif self.config.mode == "mood":
            wallpaper = self.selector.rand_mood_wallpaper(self.config.theme)
            self._update_and_apply(wallpaper)
            return wallpaper

        elif self.config.mode == "static":
            wallpaper = self.config.current_image or self.config.previous_image
            if wallpaper is None:
                raise NoValidImagesFoundError(
                    "No image found in the config file to set"
                )
            self._update_and_apply(wallpaper)
            return wallpaper
