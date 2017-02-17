from helpers import Scraper
import argparse
import os
import threading
import sys
from concurrent.futures import ThreadPoolExecutor

def main():
    print "extScrape"
    print "______________________"
    print "\n"
    parser = argparse.ArgumentParser(description='Scrape content from the web based on extension')
    parser.add_argument('url')
    parser.add_argument('extension')
    parser.add_argument('-p', dest='path', help='Specify custom path to store files')
    parser.add_argument('-m', dest='max_files', help='Limit number of files downloaded')
    parser.add_argument('-n' , dest='no_of_threads', help='Specify number of threads to spawn')
    parser.add_argument('-i', action='store_true', default=False, dest='injected', help='Scrape javascript injected content')
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
    with ThreadPoolExecutor(max_workers = scrape.max_threads) as executor:
        scrape.bar.total = scrape.total
        for i in range(0, scrape.total):
            executor.submit(scrape.download, i)
if __name__ == '__main__':
    try:
        main()
        print "\n"
        print "Done !"
        print "\n"
    except KeyboardInterrupt:
        sys.exit(0)
