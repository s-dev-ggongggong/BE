import logging
from logging.handlers import RotatingFileHandler
import os

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

def setup_logger(name):
    """Sets up a logger with both console and file handlers."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        # Formatter for log messages
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt=DATETIME_FORMAT)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Rotating File handler
        log_file_path = os.getenv('LOG_FILE_PATH', 'app.log')
        file_handler = RotatingFileHandler(log_file_path, maxBytes=1024 * 1024 * 5, backupCount=5)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Set log level (configurable via environment variable)
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        logger.setLevel(getattr(logging, log_level, logging.INFO))

        # Prevent propagation to the root logger
        logger.propagate = False

    return logger