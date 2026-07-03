import os
import tomllib
from pathlib import Path

from app.models import ConfigModel

PROJECT_DIR = Path(__file__).parent.parent
ENV_CONFIG_FILE_PATH = os.getenv("YDA_CONFIG_FILE_PATH")

if ENV_CONFIG_FILE_PATH:
    CONFIG_FILE_PATH = Path(ENV_CONFIG_FILE_PATH)
else:
    CONFIG_FILE_PATH = PROJECT_DIR / "config.yml"

assert CONFIG_FILE_PATH.exists(), (
    f"Invalid config file path {CONFIG_FILE_PATH.absolute()!r}. Does not exist"
)

import yaml
config_values = yaml.safe_load(open(CONFIG_FILE_PATH))

loaded_config = ConfigModel(**config_values)

DOWNLOAD_DIR = (
    Path(loaded_config.working_directory)
    if Path(loaded_config.working_directory).is_absolute()
    else PROJECT_DIR / loaded_config.working_directory
)

PYPROJECT_DOT_TOML_PATH = PROJECT_DIR / "pyproject.toml"
pyproject_dot_toml_details = tomllib.load(open(PYPROJECT_DOT_TOML_PATH, "rb"))
