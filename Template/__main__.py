#!/usr/bin/python3
import logging
from argparse import ArgumentParser, Namespace

from Logger import init_logger

LOGGER = logging.getLogger(__name__)

def get_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true')
    return parser.parse_args()


args = get_arguments()


def main():
    LOGGER.info("Welcome to Template - Python Edition")
    if args.test:
        LOGGER.info("You selected `--test`")


if __name__ == '__main__':
    init_logger('Template-Python')
    main()
