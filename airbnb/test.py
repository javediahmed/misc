# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 23:37:03 2019
@author: javed
"""
import os
#os.chdir('c:/files/metis/misc/airbnb')
import requests, numpy as np
from bs4 import BeautifulSoup
from bsparse import get_soup
from urllib.request import urlretrieve

output_dir = 'data/'
url = 'http://insideairbnb.com/get-the-data.html'
response = requests.get(url)
page = response.text
soup = BeautifulSoup(page, "lxml")
soup2 = get_soup(url)
links = soup.findAll('a')
l1 = links[6]
l2 = links[8]
dlinks = [x for x in links if 'csv' in str(x) or 'json' in str(x)]
dhttps = [x.attrs['href'] for x in dlinks]
hlinks = [x.attrs for x in links]

#breakpoint()

testlinks = 4
testurl = dhttps[testlinks]
filename = '_'.join(testurl.split('/')[3:])
urlretrieve(testurl, output_dir + filename)

#testfile = requests.get(dhttps[4], allow_redirects=True)
#open(output_dir + filename, 'wb').write(testfile.content)
#breakpoint()
