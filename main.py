import config
import system_statistics

import logging
import logging.config
import time


logger = logging.getLogger(__name__)
config.setup_logging()

cfg = config.load_config()

while True:
    logger.info("Battery: %d%%, CPU: %.2f%%", system_statistics.battery_percentage(), system_statistics.cpu_usage())
    time.sleep(1)