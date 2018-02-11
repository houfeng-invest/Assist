# from __future__ import print_function
# from matplotlib.font_manager import FontManager, FontProperties
# import matplotlib.pyplot as plt
# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
#
#
# def getChineseFont():
#     return FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
#
# #
# # catering_sale = './datas/catering_sale.xls'
# # data = pd.read_excel(catering_sale,index_col=u'日期')
# # # print(data.describe())
#
# # plt.figure()
# # p = data.boxplot(return_type='dict')
# #
# # x = p['fliers'][0].get_xdata()
# # y = p['fliers'][0].get_ydata()
# #
# # y.sort()
# #
# # for i in range(len(x)):
# #   if i>0:
# #     plt.annotate(y[i], xy = (x[i],y[i]), xytext=(x[i]+0.05 -0.8/(y[i]-y[i-1]),y[i]))
# #   else:
# #     plt.annotate(y[i], xy = (x[i],y[i]), xytext=(x[i]+0.08,y[i]))
# #
# #
# # plt.show()
#
# # data = data[(data[u'销量'] > 400) & (data[u'销量'] < 5000)]
# # statistics = data.describe()
# # statistics.loc['range'] = statistics.loc['max']-statistics.loc['min'] #极差
# # statistics.loc['var'] = statistics.loc['std']/statistics.loc['mean'] #变异系数
# # statistics.loc['dis'] = statistics.loc['75%']-statistics.loc['25%'] #四分位数间距
# # print(statistics)
#
#
# #初始化参数
# # dish_profit = './datas/catering_dish_profit.xls' #餐饮菜品盈利数据
# # data = pd.read_excel(dish_profit, index_col = u'菜品名')
# # print(data)
# # data = data[u'盈利'].copy()
# # # data.sort(ascending = False)
# # print(data)
# # import matplotlib.pyplot as plt #导入图像库
# # plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
# # plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
# #
# # plt.figure()
# # data.plot(kind='bar')
# # plt.ylabel(u'盈利（元）')
# # p = 1.0*data.cumsum()/data.sum()
# # p.plot(color = 'r', secondary_y = True, style = '-o',linewidth = 2)
# # plt.annotate(format(p[6], '.4%'), xy = (6, p[6]), xytext=(6*0.9, p[6]*0.9), arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2")) #添加注释，即85%处的标记。这里包括了指定箭头样式。
# # plt.ylabel(u'盈利（比例）')
# # plt.show()
#
# #
#
#
#
#
#
#
#
#
# # import  json
# #
# # path = './datas/usagov_bitly_data2012-03-16-1331923249.txt'
# # records = [json.loads(line) for line in open(path,encoding='utf-8')]
# # time_zones = [rec['tz'] for rec in records if 'tz' in rec]
# #
# # def get_counts(sequence):
# #     counts = {}
# #     for x in sequence:
# #         if x in counts:
# #             counts[x] += 1
# #         else:
# #             counts[x] = 1
# #     return  counts
# #
# #
# # from collections import defaultdict
# #
# # def get_counts2(sequence):
# #     counts = defaultdict(int)
# #     for x in sequence:
# #         counts[x] += 1
# #     return counts
# #
# # counts = get_counts(time_zones)
# #
# # def top_counts(count_dict,n=10):
# #     value_key_pairs = [(count,tz) for tz,count in count_dict.items()]
# #     value_key_pairs.sort()
# #     return value_key_pairs[-n:]
# #
# # # print(top_counts(counts))
# #
# # from collections import  Counter
# #
# # counts = Counter(time_zones)
# # #print(counts.most_common(10))
# #
# # import  matplotlib.pyplot as plt
# # from pandas import DataFrame,Series
# # import pandas as pd;import numpy as np
# # frame = DataFrame(records)
# # tz_counts = frame['tz'].value_counts()
# # # print(tz_counts[:10])
# #
# # clean_tz = frame['tz'].fillna('Missing')
# # clean_tz[clean_tz == ''] = 'Unkonwn'
# #
# # tz_counts = clean_tz.value_counts()
# #
# # # print(tz_counts[:10])
# #
# #
# # # tz_counts[:10].plot(kind="barh",rot=0)
# # # plt.show()
# #
# # results = Series([x.split()[0] for x in frame.a.dropna()])
# #
# #
# # cframe = frame[frame.a.notnull()]
# #
# # operating_system = np.where(cframe['a'].str.contains('Windows'),'Windows','Not Windows')
# # # print(operating_system[:10])
# #
# # by_tz_os = cframe.groupby(['tz',operating_system])
# # # print(by_tz_os.head())
# #
# # agg_counts = by_tz_os.size().unstack().fillna(0)
# # print(agg_counts[:10])
#
#
#
# #
# # goog = web.DataReader('GOOG',data_source='yahoo',start='1/1/2017',end='2/12/2017')
# # print(goog.tail())
# # print(dir(goog))
# # goog['Log_Ret'] = np.log(goog['Close'] / goog['Close'].shift(1))
# # goog['Volatility'] = pd.rolling_std(goog['Log_Ret'],window=252)*np.sqrt(252)
# # goog[['Close','Volatility']].plot(subplots=True,color='blue',figsize=(8,6))
# # plt.show()
#
# # from functools import *
# # import random
# # I = 5000
# # mat = [[random.gauss(0,1) for j in range(I) for i in range(I)]]
# # reduce(lambda x,y:x+y,[reduce(lambda x,y:x+y,row) for row in mat])
#
#
# import numpy  as np
# import pandas as pd
# import pandas_datareader.data as web
# import matplotlib.pylab as plt
# import re
# import matplotlib.finance as mpf
# import datetime as dt
# from matplotlib import style
# import urllib
# # import urllib3
# import requests
# # np.random.seed(1000)
# # y = np.random.standard_normal(20)
# #
# # x = range(len(y))
# # plt.plot(y.cumsum())
# # plt.grid(True)
# # # plt.axis('tight')
# # plt.xlim(-1,20)
# # plt.ylim(np.min(y.cumsum())-1,np.max(y.cumsum()+1))
# # plt.show()
#
# # plt.figure(figsize=(7,4))
# # plt.plot(y.cumsum(),'b',lw=1.5)
# # plt.plot(y.cumsum(),'ro')
# # plt.grid(True)
# # plt.axis('tight')
# # plt.xlabel('index')
# # plt.ylabel('value')
# # plt.title('A Simple Plot')
# # plt.show()
#
# # np.random.seed(2000)
# # y = np.random.standard_normal((20,2))
# # print(y)
# # y = y.cumsum(axis=0)
# # print("------------------------------------------")
# # print(y)
# # plt.figure(figsize=(7,4))
# # # plt.plot(y,lw=1.5)
# # plt.plot(y[:,0],lw=1.5,label='1st')
# # plt.plot(y[:,1],lw=1.5,label="2nd")
# # plt.legend(loc=0)
# # plt.plot(y,'ro')
# # plt.grid(True)
# # plt.axis('tight')
# # plt.xlabel('index')
# # plt.ylabel('value')
# # plt.title('A Simple Plot')
# # plt.show()
#
#
#
#
#
#
# # np.random.seed(2000)
# # y = np.random.standard_normal((20,2))
# # print(y)
# # y = y.cumsum(axis=0)
# # y[:,0] = y[:,0] *100
# # fig , ax1 = plt.subplots()
# # # plt.plot(y,lw=1.5)
# # plt.plot(y[:,0],lw=1.5,label='1st')
# # plt.plot(y[:,0],'ro')
# # plt.grid(True)
# # plt.legend(loc=8)
# # plt.axis('tight')
# # plt.xlabel('index')
# # plt.ylabel('value 1st')
# # ax2 = ax1.twinx()
# # plt.plot(y[:,1],'g',lw=1.5,label='2nd')
# # plt.plot(y[:,1],'ro')
# # plt.legend(loc=0)
# # plt.ylabel('value 1st')
# # plt.title('A Simple Plot')
# # plt.show()
#
#
# # y = np.random.standard_normal((1000,2))
# # c = np.random.randint(0,10,len(y))
# # plt.figure(figsize=(7,5))
# # # plt.plot(y[:,0],y[:,1],'ro')
# # plt.scatter(y[:,0],y[:,1],c=c,marker="o")
# # plt.grid(True)
# # plt.xlabel('1st')
# # plt.ylabel('2nd')
# # plt.title('Scatter Plot')
# # plt.show()
#
# # plt.figure(figsize=(7,4))
# # plt.hist(y,label=['1st','2nd'],color=['b','g'],stacked=True,bins=25)
# # plt.grid(True)
# # plt.legend(loc=0)
# # plt.xlabel('value')
# # plt.ylabel('frequency')
# # plt.title('Histogram')
# # fig , ax = plt.subplots(figsize=(7,4))
# # plt.boxplot(y)
# # plt.grid(True)
# # plt.setp(ax,xticklabels=['1st','2nd'])
# # plt.xlabel('data set')
# # plt.ylabel('value')
# #
# # plt.show()
#
# # df = pd.DataFrame([10,20,30,40],columns=['numbers'],index=['a','b','c','d'])
# # style.use('ggplot')
# # start = dt.datetime(2017,10,1)
# # end = dt.datetime(2017,12,4)
# #
# # df = web.DataReader('MSFT',"yahoo",start,end)
# # print(df)
#
# # a = np.random.standard_normal((9,4))
# # df = pd.DataFrame(a)
# # df.columns = ['No1','No2','No3','No4']
# # dates = pd.date_range('2017-12-1',periods=9,freq='M')
# # df.index = dates
# # df['Quarter'] = ['Q1','Q1','Q1','Q2','Q2','Q2','Q3','Q3',"Q3"]
# # print(df)
# #
# # groups = df.groupby('Quarter')
# # print(groups.mean())
# # df.cumsum().plot(lw=2.0)
# # plt.show()
#
#
#
# es_url = 'http://www.stoxx.com/download/historical_values/hbrbcpe.txt'
#
# vs_url = 'http://www.stoxx.com/download/historical_values/h_vstoxx.txt'
#
#
# # esTxt = requests.get(es_url).text
# # with open('./datas/es.txt','w') as f:
# #     f.write(esTxt)
# # vsTxt = requests.get(vs_url).text
# # with open('./datas/vs.txt','w') as f:
# #     f.write(vsTxt)
#
#
# # lines = open('./datas/es.txt','r').readlines()
# # lines = [line.replace(' ','') for line in lines]
# # # print(lines[:6])
# # with open('./datas/tmpes.txt','w') as f:
# #     f.writelines(lines)
#
# # new_file = open('./datas/es50.txt','w')
# # new_file.writelines('date'+lines[3][:-1]+';DEL'+lines[3][-1])
# # new_file.writelines(lines[4:])
# # new_file.close()
# # new_lines = open('./datas/es50.txt','r').readlines()
#
# # es = pd.read_csv('./datas/es50.txt',index_col=0,parse_dates=True,sep=';',dayfirst=True)
# # del es['DEL']
# # es.to_csv('./datas/new_es50.txt',sep=';',encoding='utf-8')
# # print(np.round(es.tail()))
#
# # es = pd.read_csv('./datas/new_es50.txt',index_col=0,parse_dates=True,sep=';',dayfirst=True)
# # vs = pd.read_csv('./datas/vs.txt',index_col=0,header=2,parse_dates=True,sep=',',dayfirst=True)
# #
# # import datetime as dt
# # data = pd.DataFrame({'EUROSTOXX':es['SX5E'][es.index > dt.datetime(1999,1,1)]})
# # data = data.join(pd.DataFrame({'VSTOXX':vs['V2TX'][vs.index > dt.datetime(1999,1,1)]}))
# # data = data.fillna(method='ffill')
# # print(data.head())
# # # data.plot(subplots=True,grid=True,figsize=(8,6))
# # # plt.show()
# #
# # import tushare as ts
# # hs300 = ts.get_hist_data('hs300')
# # zh500 = ts.get_hist_data('zh500')
# #
# # myData = pd.DataFrame({'hs300':hs300['close']})
# # myData['zh500'] = zh500['close']
# # rets = np.log(myData / myData.shift(1))
# #
# # # print(myData.head())
# # # rets.plot(subplots=True,grid=True,figsize=(8,6))
# # # plt.show()
# #
# # xdat = rets['hs300']
# # ydat = rets['zh500']
# #
# # plt.plot(xdat,ydat,'r.')
# # plt.show()
#
#
# # url1 = 'http://hopey.netfonds.no/posdump.php?'
# # url2 = 'date=%s%s%s&paper=AAPL.0&csv_format=csv'
# # url = url1 + url2
# # year = '2014'
# # month = '09'
# # days = ['22','23','24','25']
# # AAPL = pd.DataFrame()
# # for day in days:
# #     print(url % (year,month,day))
# #     AAPL = AAPL.append(pd.read_csv(url % (year,month,day), index_col = 0,header=0,parse_dates=True))
# #
# # AAPL.columns = ['bid','bdepth','bdeptht','offer','odepth','odeptht']
# #
# # print(AAPL.head())
#
# # np.polyfit()
#
# # print(np.random.rand(5,5))
# a = 5
# b = 10
# print(np.random.rand(10)*(b-a)+a)
#
# def random_from_to(f,t,num = 10):
#     return np.random.rand(num)*(t-f)+f
#
# print(random_from_to(2,4,20))

import numpy as np
np.random.seed(1000)
import scipy.stats as scs
import statsmodels.api as sm
import matplotlib as mpl
import matplotlib.pyplot as plt

def gen_paths(S0,r,sigma,T,M,I):
    dt = float(T)/M
    paths = np.zeros((M+1,I),np.float64)
    paths[0]= S0
    for t in range(1,M+1):
        rand = np.random.standard_normal(I)
        rand = (rand - rand.mean()) / rand.std()
        paths[t] = paths[t-1] * np.exp((r-0.5*sigma**2) * dt + sigma*np.sqrt(dt) *rand)
    return paths