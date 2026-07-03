from random import choice
from .config import ConfigManager
from .exceptions import NoValidImagesFoundError
from .exceptions import DirectoryNotFoundError
from .exceptions import ThemeNotSetError


class Selector:
    """
    Provides functionality for resolving paths to folders and images.
    Attributes:
        list_themes(root_dir: str)
        rand_theme()
        rand_mood_wallpaper(theme: str)
        rand_glob_wallpaper()
    """
    def __init__(self, conf: ConfigManager, supported_formats: set[str]):
        self.supported_formats = supported_formats
        self.config = conf

    def _theme_has_images(self, theme: str) -> bool:
        theme_dir = self.config.wallpapers_dir / theme
        if not theme_dir.is_dir():
            return False
        for file in theme_dir.iterdir():
            if file.suffix.lower() in self.supported_formats:
                return True
        return False

    def list_themes(self) -> list[str]:
        """
        Returns a list of themes, where each theme is the name of a directory
        inside the main wallpapers folder (the list consists of text elements)
        """
        return [d.name
                for d in self.config.wallpapers_dir.iterdir()
                if d.is_dir() and self._theme_has_images(d.name)]

    def rand_theme(self) -> str:
        valid_themes = self.list_themes()
        if not valid_themes:
            raise DirectoryNotFoundError(
                "No themes with images found in "
                f"{self.config.wallpapers_dir}")
        return choice(valid_themes)

    def rand_mood_wallpaper(self, theme: str) -> str:
        if not theme or not isinstance(theme, str) or theme.strip() == "":
            raise ThemeNotSetError("No theme specified")

        theme_dir = self.config.wallpapers_dir / theme

        if not theme_dir.is_dir():
            raise DirectoryNotFoundError(
                f"There is no directory named \"{theme}\" "
            )

        wallpapers_list = [
            str(w) for w in theme_dir.iterdir()
            if w.suffix.lower() in self.supported_formats]

        if not wallpapers_list:
            raise NoValidImagesFoundError(
                f"No valid images found in theme '{theme}'")
        
        if len(wallpapers_list) > 1 and self.config.current_image:
            cur_img_str = str(self.config.current_image)
            if cur_img_str in wallpapers_list:
                wallpapers_list.remove(cur_img_str)

        return choice(wallpapers_list)

    def rand_glob_wallpaper(self) -> str:
        return self.rand_mood_wallpaper(self.rand_theme())
