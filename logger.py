"""Shared logger module"""

import logging

__formatter = logging.Formatter(
    "[%(levelname)s] [%(module)s] [%(funcName)s:%(lineno)d] %(message)s"
)
__console_handler = logging.StreamHandler()
__console_handler.setFormatter(__formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(__console_handler)
