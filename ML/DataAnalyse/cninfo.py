
from ML.DataAnalyse import SpiderTool
from  bs4 import BeautifulSoup

g_targetUrl = 'http://www.cninfo.com.cn/cninfo-new/index'
html = SpiderTool.download(g_targetUrl)
soup = BeautifulSoup(html,'html.parser')
print(soup.prettify())
