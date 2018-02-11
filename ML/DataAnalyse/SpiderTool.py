#!/usr/bin/python3
#coding=utf-8
# -------------------------------------------------------------------------------
# Filename:    coninfo.py
# Revision:    1.0
# Date:        2017/12/21
# Author:      houfeng
# Description: analyse cninfo
# -------------------------------------------------------------------------------
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.request import Request
import urllib.robotparser as robotparser
import urllib.parse
import urllib
from bs4 import BeautifulSoup
import builtwith
import whois
import re
import itertools
import ssl
import datetime
import time
import csv
import random
ssl._create_default_https_context = ssl._create_unverified_context


def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(),'html.parser')
        title = bsObj.body.h1
    except AttributeError as e:
        return None
    return title

# title = getTitle(g_targetUrl)
# if title == None:
#     print("title could not be found")
# else:
#     print(title)

# html = urlopen(g_targetUrl)
# bsObj  = BeautifulSoup(html,'html.parser')
# fixedHtml = bsObj.prettify()
# print(fixedHtml)
#
# print(builtwith.parse(g_targetUrl))

# print(whois.whois('s.repeatlink.co.jp'))

def download(url,user_agent='ipos',num_retries=2):
    print('Downloading:',url)
    headers = {'User-agent':user_agent}
    request = Request(url,headers=headers)
    try:
        html = urlopen(request).read()
        html = str(html,encoding='utf-8')
    except HTTPError as e:
        print('Download error:',e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e,'code') and 500 <= e.code < 600:
                return download(url,num_retries=num_retries-1)
    return html




def crawl_sitemap(url):
    sitemap = download(url)
    links = re.findall('<loc>(.*?)</loc>',sitemap)
    for link in links:
        html = download(link)


def link_crawler(seed_url,link_regex,max_depth=2):
    crawl_queue = [seed_url]
    seen = {}

    while len(crawl_queue) > 0:
        url = crawl_queue.pop()
        html = download(url)
        links = get_links(html)
        depth = seen[url]
        if depth != max_depth:
            for link in links:
                if re.match(link_regex,link):
                    link = urllib.parse.urljoin(seed_url,link)
                    if link not in seen:
                        seen.setdefault(link,default=0)
                        seen[link] = depth + 1
                        crawl_queue.append(link)

def get_links(html):
    pattern = re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
    list = pattern.findall(html)
    return list




class Downloader:
    def __init__(self,delay=5,user_agent='ipos',proxies = None,num_retries=1,cache=None):
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.cache = cache

    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                pass
            else:
                if self.num_retries > 0 and 500 <= result['code'] < 600:
                    result = None
        if result is  None:
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent':self.user_agent}
            result = self.download(self,headers,proxy,self.num_retries)


        def download(self,url,headers,proxy,num_retries,data=None):
            request = Request(url,headers=headers)
            try:
                html = urlopen(request).read()
                html = str(html,encoding='utf-8')
            except HTTPError as e:
                print('Download error:',e.reason)
                html = None
            if num_retries > 0:
                if hasattr(e,'code') and 500 <= e.code < 600:
                    return self.download(url,num_retries=num_retries-1)
            return html

