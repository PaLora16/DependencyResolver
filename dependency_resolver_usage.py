from custom_logger_repo import resolve_logger
from custom_logger_repo import custom_logger_1_0_0

"""Example how to use dependency resolve_loggerr in app code
"""
# logger using classical import pattern
custom_logger_1_0_0.log_message("old fashioned Hello")

# logger using dependency resolver
logger = resolve_logger("1.0.0")
logger.log_message("cool Hello")

logger = resolve_logger("1.2.4")
logger.log_message("cool Hello")

logger = resolve_logger("latest")
logger.log_message("cool latest Hello")
