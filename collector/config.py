import logging
import os
from pathlib import Path
import sys
from typing import List, Optional

import colorlog
from appdirs import user_data_dir
from pydantic import BaseModel

from common.api_definitions import Aggregator

logger = logging.getLogger(__name__)

APP_NAME = "SystemMonitoringTool"

class Config(BaseModel):
    server_url: str
    aggregator_name: str
    device_gatherer_classes: List[str]
    num_failures_for_backoff: int
    backoff_intervals: int

class AppData(BaseModel):
    aggregator: Aggregator

CONFIG: Config | None = None

def load_config() -> Config:
    global CONFIG

    if CONFIG is None:
        logger.debug("Config not loaded; loading from file.")
        with open(os.path.join(os.path.dirname(__file__), "config.json")) as f:
            CONFIG = Config.model_validate_json(f.read())

    return CONFIG

def _get_app_data_file() -> Path:
    app_data_dir = user_data_dir(APP_NAME)
    return Path(app_data_dir) / "appdata.json"

def read_app_data() -> Optional[AppData]:
    path = _get_app_data_file()
    
    if not path.exists():
        return None
    
    with open(path) as f:
        return AppData.model_validate_json(f.read())

def write_app_data(app_data: AppData):
    path = _get_app_data_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, "w") as f:
        f.write(app_data.model_dump_json())

def setup_logging(level: int = logging.DEBUG):
    # TODO - config in file?
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
        )
    )
    logging.basicConfig(
        level=level, handlers=[logging.FileHandler("log/collector.log"), handler]
    )
