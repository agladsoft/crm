import logging

console: logging.StreamHandler = logging.StreamHandler()
logger: logging.getLogger = logging.getLogger("loggger")
if logger.hasHandlers():
    logger.handlers.clear()
logger.addHandler(console)
logger.setLevel(logging.INFO)

date_formats: tuple = ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S%z")
