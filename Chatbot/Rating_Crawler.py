import os
import re
import urllib.request

import html5lib
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize

if __name__ == '__main__':
    url = 'https://www.imdb.com/title/tt4642970/reviews'
    r = requests.get(url)

    soup = BeautifulSoup(r.content, 'html5lib')
    ratings = soup.find('div', attrs = {'class':'text show-more__control'})
    print(type(ratings))
