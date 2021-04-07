import logging
from argparse import ArgumentParser, Namespace
from time import sleep

import PyLogger
from Recommender import api, TOP_DIR

LOGGER = logging.getLogger(__name__)


def main(username: str = None, min_score: float = 7.5, min_recs: int = 10, max: int = 100, debug: bool = False):
    LOGGER.info('Welcome to MAL Recommender')
    if not api.user_authorization():
        LOGGER.error('Unable to access MAL api, check your `config.yaml`')
        return
    watchlist = api.get_watchlist(username)
    recommended = {}
    for index, (id, fields) in enumerate(watchlist.items()):
        anime = api.get_anime(id)
        if not anime:
            continue
        for rec in anime['recommendations']:
            if rec['recs'] < min_recs:
                continue
            if rec['id'] in recommended:
                recommended[rec['id']][1] += 1
            else:
                rec_anime = api.get_anime(rec['id'])
                if rec_anime:
                    if rec_anime['mean'] >= min_score:
                        LOGGER.debug(f"{rec_anime['title']} - Recommended")
                        recommended[rec_anime['id']] = [rec_anime, 1]
                    else:
                        LOGGER.debug(f"{rec_anime['title']} - Not recommended")
                sleep(2)
    LOGGER.info(f"{username or '@me'}'s Recommendations:")
    with open(TOP_DIR.joinpath(f"{username or 'me'}.csv"), 'w', encoding='UTF-8') as csv_file:
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
            if index + 1 == max:
                break


def get_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('--username', type=str, default=None)
    parser.add_argument('--min-score', type=float, default=7.5)
    parser.add_argument('--min-recs', type=int, default=10)
    parser.add_argument('--max', type=int, default=100)
    parser.add_argument('--debug', action='store_true')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_arguments()
    PyLogger.init('Recommender', console_level=logging.DEBUG if args.debug else logging.INFO)
    main(username=args.username, min_score=args.min_score, min_recs=args.min_recs, max=args.max, debug=args.debug)
