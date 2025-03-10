import logging
import os
from typing import TypeVar

from pydantic import BaseModel


logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


def load_config(config_cls: type[T], file: str, filename: str = "config.json", local_filename: str = "config.local.json") -> T:
    prod_filename = os.path.join(os.path.dirname(file), filename)
    alt_filename = os.path.join(os.path.dirname(file), local_filename)
    
    filename = alt_filename if os.path.exists(alt_filename) else prod_filename

    with open(filename) as f:
        return config_cls.model_validate_json(f.read())
