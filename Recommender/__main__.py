#!/usr/bin/python3
import logging
from argparse import ArgumentParser, Namespace
from time import sleep

from Logger import init_logger
from Recommender import api, TOP_DIR

LOGGER = logging.getLogger(__name__)


def get_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('--username', type=str, default=None)
    parser.add_argument('--score', type=float, default=6.9)
    parser.add_argument('--max', type=int, default=None)
    return parser.parse_args()


args = get_arguments()


def main():
    LOGGER.info('Welcome to MAL Recommender')
    if not api.user_authorization():
        return
    watchlist = api.get_watchlist(args.username)
    recommended = {}
    for index, (id, fields) in enumerate(watchlist.items()):
        anime = api.get_anime(id)
        if not anime:
            continue
        for rec in anime['recommendations']:
            rec_anime = api.get_anime(rec['id'])
            if rec_anime['id'] in recommended:
                LOGGER.debug(f"{rec_anime['title']} - Already Recommended {recommended[rec_anime['id']][1]}x")
                recommended[rec_anime['id']][1] += 1
            elif rec_anime['mean'] >= args.score:
                LOGGER.debug(f"{rec_anime['title']} - Recommended")
                recommended[rec_anime['id']] = [rec_anime, 1]
            else:
                LOGGER.debug(f"{rec_anime['title']} - Not recommended")
            sleep(2)
    LOGGER.info(f"{args.username or '@me'}'s Recommendations:")
    with open(TOP_DIR.joinpath(f"{args.username}.csv"), 'w', encoding='UTF-8') as csv_file:
        csv_file.write('\'title\',\'alt\',\'recs\'\n')
        recommended = {k: v for k, v in sorted(recommended.items(), key=lambda x: x[1][1])}
        for id, details in recommended.items():
            alt_title = details[0]['alternative_titles']['en'] if 'en' in details[0]['alternative_titles'] else None
            if alt_title == details[0]['title']:
                alt_title = None
            if not alt_title:
                alt_title = details[0]['alternative_titles']['ja'] if 'ja' in details[0]['alternative_titles'] else None
                if alt_title == details[0]['title']:
                    alt_title = None
            LOGGER.info(f" - {details[0]['title']} [{alt_title}] Recommended {details[1]}x")
            csv_file.write(f"\'{details[0]['title']}\',\'{alt_title}\',\'{details[1]}\'\n")


if __name__ == '__main__':
    init_logger('Recommender')
    main()
