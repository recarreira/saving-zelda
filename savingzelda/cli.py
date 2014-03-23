import argparse
import logging
from lib import SavingZelda


def main():
    parser = argparse.ArgumentParser("Check if all your webpage's links are ok. Because you can't save the day with a dead Link. \n savingzelda -u <url>")
    parser.add_argument('--url', '-u', dest="url", help="url you want to check for dead links", required=True)

    args = parser.parse_args()

    zelda = SavingZelda(args.url)
    zelda.run()


if __name__  == '__main__':
    main()