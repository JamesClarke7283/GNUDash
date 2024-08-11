import os
import sys
import logging
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from appdirs import user_log_dir
import coloredlogs

def setup_logging(app_name: str = "PixelArcade") -> logging.Logger:
    load_dotenv()
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_DIR = user_log_dir(app_name)
    os.makedirs(LOG_DIR, exist_ok=True)
    LOG_FILE = os.path.join(LOG_DIR, f"{app_name.lower()}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]",
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger(app_name)
    coloredlogs.install(level=LOG_LEVEL, logger=logger)

    # Add TRACE log level
    TRACE = 5
    logging.addLevelName(TRACE, "TRACE")
    setattr(logger, "trace", lambda message, *args: logger.log(TRACE, message, *args))

    return logger

# Global logger instance
logger: Optional[logging.Logger] = None

def get_logger() -> logging.Logger:
    global logger
    if logger is None:
        logger = setup_logging()
    return logger