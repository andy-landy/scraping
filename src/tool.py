"""
Binds command line and single srappings
"""

import argparse
import os
import random
import time

from scrap import scrap
from serp_scraper_yandex import SerpScraperYandex


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--queries-file', required=True)
    parser.add_argument('--results-count', required=True, type=int)
    parser.add_argument('--out-dir', required=True)

    return parser.parse_args()


def scrap_all(queries_file, results_count, out_dir):
    page = SerpScraperYandex(None, None)
    page.start()

    with open(queries_file, 'r') as in_:
        queries = [line.strip() for line in in_]

    for i, query in enumerate(queries):
        if i > 0:
            time.sleep(random.random() * 5 + 5)

        scrap(page, query, results_count, os.path.join(out_dir, query.replace('/', ' ').replace(' ', '_')))
    
    page.close()


def main():
    args = parse_args()

    scrap_all(args.queries_file, args.results_count, args.out_dir)


if __name__ == '__main__':
    main()
