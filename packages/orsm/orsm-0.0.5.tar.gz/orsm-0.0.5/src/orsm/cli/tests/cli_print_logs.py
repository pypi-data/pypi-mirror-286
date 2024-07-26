#!/usr/bin/env python3

from orsm.cli import cli
from orsm.variables.variables import variable_names_and_objects
from orsm.logger.logger import log as logging
from time import sleep


def main(**kwargs):
    for name, logger in variable_names_and_objects(logging.trace, logging.debug, logging.info, logging.print, logging.warning, logging.error, logging.critical, vars_only=True):
        sleep(0.01)  # So we can see the timestamp increments more clearly.
        logger(f"A message from {name}")


if __name__ == "__main__":
    parser = cli.setup_standard_parser()
    kwargs = vars(parser.parse_args())
    main(**kwargs)
