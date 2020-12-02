import os, requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from urllib.error import HTTPError
from datetime import datetime
from lxml import html

URL = 'repos.html'

from download import find_links

tree = html.parse(URL)

print(tree)


