from random import choice
from .config import ConfigManager
from .exceptions import NoValidImagesFoundError
from .exceptions import DirectoryNotFoundError
from .exceptions import ThemeNotSetError


class Selector:
    """
    Provides functionality for resolving paths to folders and images.
    Atributes:
        list_themes(root_dir: str)
        rand_theme()
        rand_mood_wallpaper(theme: str)
        rand_glob_wallpaper()
    """
    def __init__(self, conf: ConfigManager):
        self.config = conf

    def list_themes(self) -> list[str]:
        """
        Returns a list of themes, where each theme is the name of a directory
        inside the main wallpapers folder (the list consists of text elements)
        Params:
            root_dir (str): A wallpaper folder.
        """
        return [d.name
                for d in self.config.wallpapers_dir.iterdir()
                if d.is_dir()]

    def rand_theme(self) -> str:
        themes = self.list_themes()
        if themes:
            return choice(themes)
        else:
            raise DirectoryNotFoundError("There aren't any directories in "
                                         f"{self.config.wallpapers_dir}")

    def rand_mood_wallpaper(self, theme: str) -> str:
        wallpapers_dir = self.config.wallpapers_dir
        if not theme:
            raise ThemeNotSetError(
                "No theme specified and no default theme in configuration"
            )
        if not (wallpapers_dir / theme).is_dir():
            raise DirectoryNotFoundError(
                f"There is no a directory named \"{theme}\" "
            )
        wallpapers_list = [
            w
            for w in (wallpapers_dir / theme).iterdir()
            if w.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}]
        wallpaper = str(choice(wallpapers_list)) if wallpapers_list else None
        if not wallpaper:
            raise NoValidImagesFoundError("There aren't any images in "
                                          f"{str(wallpapers_dir)}/{theme}")
        return wallpaper

    def rand_glob_wallpaper(self) -> str:
        return self.rand_mood_wallpaper(self.rand_theme())
