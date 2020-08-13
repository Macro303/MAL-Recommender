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
    parser.add_argument('--score', type=float, default=7.5)
    parser.add_argument('--recs', type=int, default=10)
    parser.add_argument('--max', type=int, default=100)
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
            if rec['recs'] < args.recs:
                continue
            if rec['id'] in recommended:
                recommended[rec['id']][1] += 1
            else:
                rec_anime = api.get_anime(rec['id'])
                if rec_anime:
                    if rec_anime['mean'] >= args.score:
                        LOGGER.debug(f"{rec_anime['title']} - Recommended")
                        recommended[rec_anime['id']] = [rec_anime, 1]
                    else:
                        LOGGER.debug(f"{rec_anime['title']} - Not recommended")
                sleep(2)
    LOGGER.info(f"{args.username or '@me'}'s Recommendations:")
    with open(TOP_DIR.joinpath(f"{args.username or 'me'}.csv"), 'w', encoding='UTF-8') as csv_file:
        csv_file.write('\'title\',\'alt\',\'recs\'\n')
        recommended = {k: v for k, v in sorted(recommended.items(), key=lambda x: x[1][1], reverse=True)}
        for index, (id, details) in enumerate(recommended.items()):
            alt_title = details[0]['alternative_titles']['en'] if 'en' in details[0]['alternative_titles'] else None
            if alt_title == details[0]['title']:
                alt_title = None
            if not alt_title:
                alt_title = details[0]['alternative_titles']['ja'] if 'ja' in details[0]['alternative_titles'] else None
                if alt_title == details[0]['title']:
                    alt_title = None
            LOGGER.info(f" - {details[0]['title']} [{alt_title}] Recommended {details[1]}x")
            csv_file.write(f"\'{details[0]['title']}\',\'{alt_title}\',\'{details[1]}\'\n")
            if index + 1 == args.max:
                break


if __name__ == '__main__':
    init_logger('Recommender')
    main()
