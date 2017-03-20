import requests
from lxml import html
import os
import sys


class Scraper:

    def __init__(self):
        self.url = None
        self.ext = None
        self.html = None
        self.path = None
        self.image_scrape = None
        self.max_threads = 1
        self.links = []
        self.max = 100000
        self.total = 0
        self.done = 0
        self.injected = False

    def get_source(self):
        try:
            r = requests.get(self.url)
        except requests.exceptions.MissingSchema:
            r = requests.get('http://' + self.url)
        except requests.exceptions.ConnectionError:
            print "Connection error"
            sys.exit(0)
        self.html = r.content

    def scan_links(self):
        tree = html.fromstring(self.html)
        link_list = tree.xpath('//a//@href')
        if self.image_scrape:
            link_list += tree.xpath('//img//@src')
        for link in link_list:
            if link.endswith(self.ext):
                self.links.append(link)
        self.total = len(self.links)
        if self.total > self.max:
            self.total = self.max
        print "Found :", self.total

    def download(self, index):
        url = self.links[index]
        try:
            dload = requests.get(url, stream=True)
        except requests.exceptions.MissingSchema:
            import urlparse
            url = urlparse.urljoin(self.url, url)
            dload = requests.get(url, stream=True)
        except requests.exceptions.ConnectionError:
            print "Connection error"
            sys.exit()
        filename = url.split('/')[-1]
        filename = requests.utils.unquote(filename)
        with open(os.path.join(self.path, filename), 'wb') as f:
            for chunk in dload.iter_content(chunk_size=34):
                f.write(chunk)
        self.done += 1
        self.bar.update(1)
        return index

    def checkIfImage(self):
        image_extensions = ('jpg', 'jpeg', 'png', 'gif', 'svg')
        if self.ext.endswith(image_extensions):
            self.image_scrape = True
