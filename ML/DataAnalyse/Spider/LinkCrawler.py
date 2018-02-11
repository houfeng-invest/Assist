import re
import urllib.parse
import urllib
import time
import datetime
import urllib.robotparser as robotparser
from ML.DataAnalyse.Spider.Downloader import  Downloader

def link_crawler(seed_url,link_regex=None,delay=5,max_depth=-1,max_urls=-1,user_agent='ipos',proxies=None,num_retries=1,scrape_callback=None,cache=None):
    crawl_queue = [seed_url]
    seen = {seed_url:0}
    num_urls = 0
    rp = get_robots(seed_url)
    D = Downloader(delay=delay,user_agent=user_agent,proxies=proxies,num_retries=num_retries,cache=cache)
    while len(crawl_queue) > 0 :
        url = crawl_queue.pop()
        depth = seen[url]
        if rp.can_fetch(user_agent,url):
            html = D(url)
            links = []
            if scrape_callback:
                links.extend(scrape_callback(url,html) or [])
            if depth != max_depth:
                if link_regex:
                    links.extend(link for link in get_links(html) if re.match(link_regex,link))
                for link in links:
                    link = normalize(seed_url,link)
                    if link not in seen:
                        seen[link] = depth + 1
                        if same_domain(seed_url,link):
                            crawl_queue.append(link)

                num_urls += 1
                if num_urls == max_urls:
                    break
        else:
            print('Blocked by robots.txt',url)



def normalize(seed_url,link):
    link,_ = urllib.parse.urldefrag(link)
    return urllib.parse.urljoin(seed_url,link)

def same_domain(url1,url2):
    return urllib.parse(url1).netloc == urllib.parse.urlparse(url2).netloc

def get_robots(url):
    rp = robotparser.RobotFileParser()
    rp.set_url(urllib.parse.urljoin(url,'/robots.txt'))
    rp.read()
    return rp

def get_links(html):
    webpage_regex = re.compile('<a\s+href=["\'](.*?)["\']'.re.I)
    return webpage_regex.findall(html)
