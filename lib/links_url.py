# -*- coding: utf-8 -*-
"""
Created on Wed 7/9/2020
@author: javed
"""
import os, sys, requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from urllib.error import HTTPError
from datetime import datetime

if len(sys.argv) > 1:
    URL = sys.argv[1]
else:
    print("Usage: python <url> <outputfile>")
if len(sys.argv) > 2:
    OUTPUT = sys.argv[2]

def find_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    return(soup.findAll('a'))

def parse_links(linklist, url_only=True):
    datalinks = []
    if url_only:
        datalinks.append(link.attrs['href'])
    else: 
        datalinks.append(link)
    return(datalinks)
    
# def data_links(linklist, datatypes=['csv'], url_only=True):
#     datalinks = []
#     for link in linklist:
#         for dtype in datatypes:         
#             if dtype in str(link):
#                 if url_only:
#                     datalinks.append(link.attrs['href'])
#                 else: 
#                     datalinks.append(link)
        
#     return(datalinks)            

def main(url=URL, output=OUTPUT):
    links = find_links(url)
    datalinks = parse_links(links, datatypes=['csv', 'json'])
    link_filenames = ['_'.join(link.split('/')[3:]) for link in datalinks]

if __name__ == '__main__':
    start = datetime.now()
    main()
    end = datetime.now()
    time = end - start
    print('Start: ', str(start)[:-7])
    print('End:   ', str(end)[:-7])    
    print(f'Time:   {round(time.total_seconds()/60, 1)} minutes')    
