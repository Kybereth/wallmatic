class ThemeNotSetError(Exception):
    """Raised when a mood/theme operation
    is requested without a theme being set."""
    pass


class ConfigError(Exception):
    """Configuration Error"""
    pass


class DependencyMissingError(Exception):
    """
    Raised when a required depency is missing.
    """


class NoValidImagesFoundError(Exception):
    """No valid images found in a directory or theme."""
    pass


class DirectoryNotFoundError(Exception):
    """
    Raised when a required directory doesn't exist ot is inaccessible.
    """
    def __init__(self, message: str, path: str | None = None):
        super().__init__(message)
        self.path = path

    def __str__(self) -> str:
        if self.path:
            return f"{self.args[0]} (path: {self.path})"
        return self.args[0]
