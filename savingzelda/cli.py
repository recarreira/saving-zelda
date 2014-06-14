import argparse
import logging
from lib import SavingZelda


def main():
    parser = argparse.ArgumentParser("Check if all your webpage's links are ok. Because you can't save the day with a dead Link. \n savingzelda -u <url>")
    parser.add_argument('--url', '-u', dest="url", help="url you want to check for dead links", required=True)

    parser.add_argument('--verbose', '-v', action='store_true', dest="verbose", help="Verbose output", default=False)
    parser.add_argument('--log', dest="log_path", help="log file path", default=None)

    args = parser.parse_args()

    logger = get_logger(args.log_path, args.verbose)
    zelda = SavingZelda(args.url, logger)
    zelda.run()


def get_logger(log_path, verbose):
    level = logging.DEBUG if verbose else logging.INFO

    handler, message = get_logger_handler(log_path)
    formatter = logging.Formatter(message)
    handler.setFormatter(formatter)
    logger = logging.getLogger("savingzelda")
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


def get_logger_handler(log_path):
    if log_path is None:
        return logging.StreamHandler(), '%(message)s'
    else:
        return logging.FileHandler(log_path), '%(asctime)s %(message)s'


if __name__  == '__main__':
    main()