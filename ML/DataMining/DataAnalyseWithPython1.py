# import pandas as pd
# names = ['Bob','Jessica','Mary','John','Mel']
# grades = [76,95,77,78,99]
# GradeList = list(zip(names,grades))
# print(GradeList)
# df = pd.DataFrame(data = GradeList, columns=['Names','Grades'])
# df.to_csv('studentgrades.csv',index=False,header=True)

import numpy as np
import matplotlib.pyplot as plt
from pylab import *

def is_outlier(points,threshold=3.5):
    if len(points.shape) == 1:
        points=points[:,None]
    median = np.median(points,axis=0)
    diff = np.sum((points - median)**2,axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)
    modified_z_score = 0.6745 * diff / med_abs_deviation
    return modified_z_score > threshold


# x = np.random.random(100)
# buckets = 50
# x = np.r_[x,-49,95,100,-100]
# filtered = x[~is_outlier(x)]

# plt.figure()
# plt.subplot(211)
# plt.hist(x,buckets)
# plt.xlabel("Raw")
# plt.subplot(212)
# plt.hist(filtered,buckets)
# plt.xlabel("Cleaned")
# plt.show()

# a = np.array([1,2,3,4,5])
# print(a)
# a = a[:,None]
# median = np.median(a,axis=0)
# print(median)
# diff = np.sum((a - median)**2,axis=-1)
# diff = np.sqrt(diff)
# print(diff)
#
# med_abs_deviation = np.median(diff)
# print(med_abs_deviation)
# modified_z_score = 0.6745 * diff / med_abs_deviation
# print(modified_z_score)
#

# spread = rand(50) * 100
# center = ones(25)*50
#
# flier_high = rand(10) * 100 + 100
# flier_low = rand(10) * - 100
# data = concatenate((spread,center,flier_high,flier_low),0)
# subplot(311)
# boxplot(data,0,'gx')
#
# subplot(312)
# spread_1 = concatenate((spread,flier_high,flier_low))
# center_1 = ones(70)*25
# scatter(center_1,spread_1)
# xlim([0,50])
#
# subplot(313)
# center_2 = rand(70) * 50
# scatter(center_2, spread_1)
# xlim([0, 50])
#
# show()

import sys

filename = sys.argv[1]

with open(filename,'rb') as hugefile:
    chunksize = 1000
    readable = ''
    while hugefile:
        start = hugefile.tell()
        print('')
        file_block = ''
        for _ in range(start,start + chunksize):
            line= hugefile.next()
            file_block = file_block + line
        readable = readable + file_block
        stop = hugefile.tell()
        







































