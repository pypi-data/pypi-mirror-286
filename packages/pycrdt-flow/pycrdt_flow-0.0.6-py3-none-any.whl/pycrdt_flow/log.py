import os

USER_DEFINED_LOG_LEVEL = os.getenv("PYCRDT_FLOW_LOG_LEVEL", "DEBUG")

os.environ["LOGURU_LEVEL"] = USER_DEFINED_LOG_LEVEL

from loguru import logger
