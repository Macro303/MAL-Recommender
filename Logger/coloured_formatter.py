#!/usr/bin/env python3
import logging
from logging import Formatter


class ColouredFormatter(Formatter):
    MAPPING = {
        logging.NOTSET: 34,  # Blue
        logging.DEBUG: 32,  # Green
        logging.INFO: 37,  # White
        logging.WARNING: 33,  # Yellow
        logging.WARN: 33,  # Yellow
        logging.ERROR: 31,  # Red
        logging.CRITICAL: 35,  # Magenta
        logging.FATAL: 35  # Magenta
    }
    PREFIX = '\033['
    SUFFIX = '\033[0m'
    FORMAT = '[%(asctime)s] [%(levelname)-8s] {%(name)s:%(filename)s} | %(message)s'

    def format(self, record):
        seq = self.MAPPING.get(record.levelno, 37)  # Default INFO
        log_fmt = '{0}{1}m{2}{3}'.format(self.PREFIX, seq, self.FORMAT, self.SUFFIX)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
