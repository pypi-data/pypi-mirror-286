import os
import sys

from loguru import logger

__version__ = "1.5.5"
assert sys.version_info >= (3, 8)

logger.remove()
level = os.getenv("DLL")  # dspawpy log level
if level:  # default to simulate no log
    logger.add(
        sys.stderr,
        level=level,
        format="<green>{time:MM-DD HH:mm:ss:SSS}</green> | <level>{message}</level>",
    )
else:
    logger.add(
        sys.stderr,
        colorize=True,
        format="<level>{message}</level>",
    )

logger.add(
    ".dspawpy.log",
    level="DEBUG",
    rotation="1 day",
    retention="1 week",
    compression="zip",
)
