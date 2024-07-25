# log_config.py

import logging
import os
def setup_logging():
    """Set up the logging configuration."""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Console output
            logging.FileHandler(os.getenv('SCRAPER_LOG_FILE', 'scraper.log'))  # File output
        ]
    )
    # Additional configuration
    logger = logging.getLogger(__name__)
    logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))  # Set the root logger level to DEBUG

    # Adding a custom formatter for handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    for handler in logger.handlers:
        handler.setFormatter(formatter)
