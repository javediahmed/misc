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
else:
    OUTPUT = URL.replace("https:", "").replace("/", "").replace("http:","").replace(":","") + ".links.txt"
    
def find_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    return(soup.findAll('a'))

def parse_links(linklist):
    datalinks = []
    titles = []
    for link in linklist:
        if link.attrs['href'] != "#":
            datalinks.append(link.attrs['href'])
            titles.append(link.text.replace("\n", ""))
    return(datalinks, titles)
    
def main(url=URL, output=OUTPUT):
    links = find_links(url)
    datalinks, titles = parse_links(links)
    breakpoint()
    for l, link in enumerate(datalinks):
        if "on24" in link.lower():
            print(f'{link}, {titles[l]}', file=open(OUTPUT, 'a'))

if __name__ == '__main__':
    start = datetime.now()
    main()
    end = datetime.now()
    time = end - start
    print('Start: ', str(start)[:-7])
    print('End:   ', str(end)[:-7])    
    print(f'Time:   {round(time.total_seconds()/60, 1)} minutes')    
