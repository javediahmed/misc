import pyforest
import requests
from pprint import pprint as p
from bs4 import BeautifulSoup

URLS = ('http://theflameofhope.co/lady%20gaga/', '')

##
URL = URLS[0]

r = requests.get(URL)
s = BeautifulSoup(r.content)

p(s.prettify())
