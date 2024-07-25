from orsm.logger.logger import log as logging
from orsm.logger.logger import set_logging_level
from orsm.variables.variables import variable_names_and_objects
from time import sleep

if __name__ == "__main__":
    set_logging_level(level=logging.TRACE)
    for name, logger in variable_names_and_objects(logging.trace, logging.debug, logging.info, logging.print, logging.warning, logging.error, logging.critical):
        sleep(0.01)  # So we can see the timestamp increments more clearly.
        logger(f"A message from {name}")