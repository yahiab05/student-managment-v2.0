from platformdirs import user_config_dir
from pathlib import Path

APP_NAME = "dar_coran"
APP_AUTHOR = "Dar_Coran"

CONFIG_DIR = Path(user_config_dir(APP_NAME, APP_AUTHOR))
CONFIG_FILE = CONFIG_DIR / "db.ini"