import logging
import logging.config

import json
import sys

class StdWriter(object):
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level

    def write(self, text):
        self.logger.log(self.level, text)


def get_logger(config_file_name, name):
    with open(config_file_name) as f:
        content = f.read()
    config_data = json.loads(content)

    logging.config.dictConfig(config_data)

    logger = logging.getLogger(name)

    sys.stderr = StdWriter(logger, logging.ERROR)
    sys.stdout = StdWriter(logger, logging.WARNING)

    return logger

