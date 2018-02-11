import  pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
HSRet300 = pd.read_csv('./datas/return300.csv')
# density = stats.gaussian_kde(HSRet300.iloc[:,1])
# print(HSRet300.iloc[:,1].head(n=2))
# print(density)
# print(HSRet300.head(n=2))
#
# bins = np.arange(-5,5,0.02)
# plt.subplot(211)
# plt.plot(bins,density(bins))
# plt.subplot(212)
# plt.plot(bins,density(bins).cumsum())
# plt.show()

print(HSRet300.head())

ret = HSRet300.iloc[:,1]
print(ret.head())
p = len(ret[ret>0])/len(ret)
print(p)

prob = stats.binom.pmf(6,10,p)
print(prob)
