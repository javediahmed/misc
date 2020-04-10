# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 23:37:03 2019
@author: javed
"""
import requests, numpy as np
from bs4 import BeautifulSoup

def get_soup(url):
    """
    This function parses a URL and returns the HTML code
    ---
    Input: URL (string)
    Output: HTML code (bs4.BeautifulSoup object)
    """
    UAS = (
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko\
        /20100101 Firefox/40.1",
        "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101\
        Firefox/36.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0)\
        Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 \
        Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    )

    ua = UAS[np.random.randint(0, len(UAS))]

    headers = {'user-agent': ua}
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if str(response.status_code)[0] != '2':
        print('Check status code = {}'.format(response.status_code))
        return
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

