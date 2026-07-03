import logging
from pathlib import Path

LOG_DIR = Path.home() / ".config" / "wallmatic"
LOG_FILE = LOG_DIR / "wallmatic.log"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("wallmatic")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
