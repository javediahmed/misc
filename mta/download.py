# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 23:37:03 2019
@author: javed
"""
import os, requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from urllib.error import HTTPError
from datetime import datetime

URL = 'http://web.mta.info/developers/turnstile.html'
LINK_STEM = 'http://web.mta.info/developers/'
OUTPUT_DEST = 'data/'
START_FILE = None
OUTPUT_LINKS = 'mta_links.txt'

def find_links(url):
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "lxml")
    return(soup.findAll('a'))

def parse_links(linklist, datatypes=['csv'], url_only=True, link_stem=None):
    datalinks = []
    for link in linklist:
        for dtype in datatypes:
            if dtype in str(link):
                if url_only:
                    datalinks.append(link.attrs['href'])
                else: 
                    datalinks.append(link)
    return(datalinks)            

def main(url=URL, output_dir=OUTPUT_DEST, unzip=True, start_file=START_FILE, stem=LINK_STEM):
    links = find_links(url)
    datalinks = parse_links(links, datatypes=['txt'])
    link_filenames = ['_'.join(link.split('/')[3:]) for link in datalinks]
    if start_file is not None and start_file in link_filenames:
        start_num = link_filenames.index(start_file)
    else: start_num = 0
    link_targets = datalinks[start_num:]
    link_filenames = link_filenames[start_num:]
    link_errors = []
    breakpoint()
    print("Writing files:")
    for l, link in enumerate(link_targets):
        #link_filename = '_'.join(link.split('/')[3:])
        print(f'{link_filenames[l]}')
        print(f'{link_filenames[l]}', file=open(OUTPUT_LINKS, 'a'))
        try:
            urlretrieve(stem + link, output_dir + link_filenames[l])           
        except:
            print(f'** Error: {link_filenames[l]}')
            print(f'** Error: {link_filenames[l]}', file=open(OUTPUT_LINKS, 'a'))
            link_errors.append(link_filenames[l])
    print(f'Files with errors ({len(link_errors)} of {len(link_targets)}):')
    for error in link_errors:
        print(error)
      
if __name__ == '__main__':
    start = datetime.now()
    main()
    end = datetime.now()
    time = end - start
    print('Start: ', str(start)[:-7])
    print('End:   ', str(end)[:-7])    
    print(f'Time:   {round(time.total_seconds()/60, 1)} minutes')    
    
