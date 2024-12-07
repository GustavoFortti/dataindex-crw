import logging
import json
from typing import Union, Dict, Any


def setup_logging(log_file: str = 'app.log') -> None:
    """
    Sets up the logging system to record messages to a file and the console.
    
    Args:
        log_file (str): Path to the log file. Defaults to 'app.log'.
    """
    # Basic configuration for the log file
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    # Optional: Additional configurations for specific handlers can be added here
    # For example, setting different levels for file and console
    # logger = logging.getLogger()
    # logger.handlers[0].setLevel(logging.DEBUG)  # File
    # logger.handlers[1].setLevel(logging.INFO)   # Console


def message(msg: Union[str, Dict[str, Any]], level: str = 'info') -> None:
    """
    Logs a message. Accepts strings or dictionaries.
    
    Args:
        msg (Union[str, Dict[str, Any]]): Message to be logged. Can be a string or a dictionary.
        level (str): Logging level ('debug', 'info', 'warning', 'error', 'critical'). Defaults to 'info'.
    """
    logger: logging.Logger = logging.getLogger()

    # Serialize dictionaries to JSON
    if isinstance(msg, dict):
        try:
            msg = json.dumps(msg, ensure_ascii=False)
        except (TypeError, ValueError) as e:
            e: Exception
            logger.error(f"Failed to serialize dictionary to JSON: {e}")
            msg = str(msg)  # Fallback to string if serialization fails

    # Map the logging level to the corresponding methods
    level = level.lower()
    if level == 'debug':
        logger.debug(msg)
    elif level == 'info':
        logger.info(msg)
    elif level == 'warning':
        logger.warning(msg)
    elif level == 'error':
        logger.error(msg)
    elif level == 'critical':
        logger.critical(msg)
    else:
        logger.info(msg)  # Fallback to 'info' if the level is unknown


setup_logging()
