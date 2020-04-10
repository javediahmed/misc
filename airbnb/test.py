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
START_FILE = 'greece_crete_crete_2019-02-16_data_listings.csv.gz'

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

def main(url=URL, output_dir=OUTPUT_DEST, unzip=True, start_file=START_FILE):
    links = find_links(url)
    datalinks = parse_links(links, datatypes=['csv', 'json'])
    link_filenames = ['_'.join(link.split('/')[3:]) for link in datalinks]
    if start_file is not None and start_file in link_filenames:
        start_num = link_filenames.index(start_file)
    else: start_num = 0
    link_targets = datalinks[start_num:]
    link_errors = []
    #breakpoint()
    print("Writing files:")
    for l, link in enumerate(links_targets):
        #link_filename = '_'.join(link.split('/')[3:])
        print(f'{link_filename}')
        try:
            urlretrieve(link, output_dir + link_filename)           
        except HTTPError:
            print('** HTTP Error: {link_filename}')
            link_errors.append(link_filename)
    print(f'Files with errors ({len(link_errors)} of {len(datalinks_target)}):')
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
    
