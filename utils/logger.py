import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    # Ensure logs directory exists
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger("SmartMeterLogger")
    logger.setLevel(logging.DEBUG)

    # Formatter
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(module)s] - %(message)s')

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handlers
    log_files = {
        "application.log": logging.INFO,
        "communication.log": logging.DEBUG,
        "database.log": logging.INFO,
        "error.log": logging.ERROR
    }

    for log_file, level in log_files.items():
        handler = RotatingFileHandler(
            os.path.join(log_dir, log_file),
            maxBytes=10*1024*1024, # 10MB
            backupCount=5
        )
        handler.setFormatter(formatter)
        handler.setLevel(level)
        logger.addHandler(handler)

    return logger

# Global logger instance
logger = setup_logger()
