from helpers import Scraper
import argparse
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import threading


def main():
    try:
        console()
    except KeyboardInterrupt:
        print ("Scraping stopped by user.")
        sys.exit(0)


def console():
    print "extscrape"
    print "*********************"
    print "\n"
    parser = argparse.ArgumentParser(
        description='Scrape content from the web based on extension')
    parser.add_argument('url')
    parser.add_argument('extension')
    parser.add_argument('-p', dest='path',
                        help='Specify custom path to store files')
    parser.add_argument('-m', dest='max_files',
                        help='Limit number of files downloaded')
    parser.add_argument('-n', dest='no_of_threads',
                        help='Specify number of threads to spawn')
    parser.add_argument('-i', action='store_true', default=False,
                        dest='injected',
                        help='Scrape javascript injected content')
    results = parser.parse_args()
    scrape = Scraper()
    scrape.url = results.url
    scrape.injected = results.injected
    if results.no_of_threads:
        scrape.max_threads = results.no_of_threads
    if results.max_files:
        scrape.max = int(results.max_files)
    if results.path:
        scrape.path = results.path
    else:
        scrape.path = './' + results.url.split('/')[2] + '_scrape'
    if scrape.path:
        if not os.path.exists(scrape.path):
            try:
                os.makedirs(scrape.path)
            except OSError:
                print "Permission denied. Check your path."
                sys.exit(0)
        if not os.access(scrape.path, os.W_OK):
            print "Permission denied. Check your path."
            sys.exit(0)
    scrape.ext = results.extension
    scrape.get_source()
    scrape.scan_links()
    scrape.bar = tqdm(bar_format='{percentage:3.0f}%|{bar}|{n_fmt}/{total_fmt} \
                        ETA {remaining}')
    executor = ThreadPoolExecutor(max_workers=scrape.max_threads)
    scrape.bar.total = scrape.total
    for i in range(0, scrape.total):
        executor.submit(scrape.download, i)
    executor.shutdown()
    print "\n"
    print "Done !"
    print "\n"


if __name__ == '__main__':
    main()

