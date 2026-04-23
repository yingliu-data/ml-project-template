import logging
import os
from datetime import datetime

_LOG_FORMAT = "[ %(asctime)s ] %(filename)s:%(lineno)d %(funcName)s %(levelname)s - %(message)s"


def get_logger(name: str = "package_name", log_level: int = logging.INFO, log_dir: str = "logs"):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    formatter = logging.Formatter(_LOG_FORMAT)

    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(log_level)
    logger.propagate = False
    return logger
