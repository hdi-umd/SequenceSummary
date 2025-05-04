"""Structured logging module for all techniques."""

import logging
import os
import time
from datetime import datetime


def setup_logger(name, technique_name):
    """
    Set up a logger with consistent formatting.

    Args:
        name (str): Logger name, typically __name__ from the calling module
        technique_name (str): Name of the technique (CoreFlow, SentenTree, etc.)

    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create timestamp for log filename
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = f"{log_dir}/{technique_name}_{timestamp}.log"

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Clear any existing handlers (to avoid duplicates)
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
