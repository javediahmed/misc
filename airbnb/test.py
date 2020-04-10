# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 23:37:03 2019
@author: javed
"""
import os, requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from datetime import datetime

URL = 'http://insideairbnb.com/get-the-data.html'
OUTPUT_DEST = 'data/'

def find_links(url):
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "lxml")
    return(soup.findAll('a'))

def parse_links(linklist, datatypes=['csv'], url_only=True):
    datalinks = []
    for link in linklist:
        for dtype in datatypes:
            if dtype in str(link):
                if url_only:
                    datalinks.append(link.attrs['href'])
                else: 
                    datalinks.append(link)
    return(datalinks)            

def main(url=URL, output_dir=OUTPUT_DEST, unzip=True):
    links = find_links(url)
    datalinks = parse_links(links, datatypes=['csv', 'json'])
    print("Writing files:")
    for link in datalinks[:5]:
        link_filename = '_'.join(link.split('/')[3:])
        print(f'{link_filename}')
        urlretrieve(link, output_dir + link_filename)
      
if __name__ == '__main__':
    start = datetime.now()
    main()
    end = datetime.now()
    time = end - start
    print('Start: ', str(start)[:-7])
    print('End:   ', str(end)[:-7])    
    print(f'Time:   {round(time.total_seconds()/60, 1)} minutes')    
    


#from bsparse import get_soup
#response = requests.get(url)
#page = response.text
#soup = BeautifulSoup(page, "lxml")
#soup2 = get_soup(url)
#links = soup.findAll('a')
#l1 = links[6]
#l2 = links[8]
#dlinks = [x for x in links if 'csv' in str(x) or 'json' in str(x)]
#dhttps = [x.attrs['href'] for x in dlinks]
#hlinks = [x.attrs for x in links]
#testurl = dhttps[testlinks]
#filename = '_'.join(testurl.split('/')[3:])
#urlretrieve(testurl, output_dir + filename)

