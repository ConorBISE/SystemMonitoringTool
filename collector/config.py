from pydantic import BaseModel
import colorlog

import sys
import logging
import os

logger = logging.getLogger(__name__)

class Config(BaseModel):
    a: int
    
CONFIG: Config | None = None
    
def load_config() -> Config:
    global CONFIG

    if CONFIG is None:        
        logger.debug("Config not loaded; loading from file.")
        with open(os.path.join(os.path.dirname(__file__), "config.json")) as f:
            CONFIG = Config.model_validate_json(f.read())
        
    return CONFIG

def setup_logging(level: int = logging.DEBUG):
    # TODO - config in file?
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(colorlog.ColoredFormatter("%(log_color)s[%(asctime)s] %(levelname)s:%(name)s:%(message)s"))
    logging.basicConfig(level=level, handlers=[logging.FileHandler("log/collector.log"), handler])
