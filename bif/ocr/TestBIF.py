from bif.logger import log_level, logger

# CRITICAL
# FATAL
# ERROR
# WARNING
# WARN
# INFO
# DEBUG

log_level("INFO")

logger.critical("Running core ocr")
logger.error("Running core ocr")
logger.warning("Running core ocr")
logger.info("Running core ocr")
logger.debug("Running core ocr")
