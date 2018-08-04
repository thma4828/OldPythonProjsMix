import bs4
from bs4 import BeautifulSoup
import requests
import csv
import glob
from urllib.request import Request, urlopen

def main():
    url = 'http://www.cnn.com/sitemaps/sitemap-articles-2017-06.xml'
    request = Request(url, headers={'User-Agent':'Mozilla/5.0'})
    source = urlopen(request).read()
    soup = bs4.BeautifulSoup(source, 'xml')
    print(soup)

        