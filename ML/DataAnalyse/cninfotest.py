import sys
from ML.DataAnalyse import SpiderTool
import re
from  bs4 import BeautifulSoup

#.*/(index|view)$
# link_crawler('http://example.webscraping.com','.*/(index|view)$')
# match = re.match(".*/(index|view)$","/places/default/index")
# print(match)
# pattern = re.compile('[abcd]{4}[\w]+$ad',re.IGNORECASE)
# pattern = re.compile('h\w*d',re.IGNORECASE)
# pattern = re.compile('<a\s+href=["\'](.*)["\']')

# match = pattern.search('badc helloworld ,addcdad awdahello,adaafd ,hellowdad')
# print(match.group())
# print(match.endpos)
# list = pattern.findall('''var ajax_error_500 = 'An error occured, please <a href="/places/default/index">reload</a> the page''')
# print(list)


# link_crawler('http://example.webscraping.com','.*/(index|view)$')

# rp = robotparser.RobotFileParser()
# rp.set_url(g_targetUrl+'robots.txt')
# url = g_targetUrl
# user_agent = 'BadCrawler'
# print(rp.can_fetch(user_agent,url))
# print(urllib.parse.urlparse(g_targetUrl).netloc)

url = 'http://example.webscraping.com/view/United-Kingdom-239'
url = 'http://www.cninfo.com.cn/cninfo-new/index'
html = SpiderTool.download(url)

soup = BeautifulSoup(html,'html.parser')
print(soup.prettify())




