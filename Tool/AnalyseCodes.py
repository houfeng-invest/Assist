import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

currentPath = os.path.abspath('.')
g_filenames = []
g_lines = []

def analyse(path):
    for i in os.listdir(path):
        subPath = path+"/"+i
        if os.path.isdir(subPath):
            analyse(subPath)
        else:
            sp = os.path.splitext(subPath)
            if len(sp) > 1 :
                if sp[1] == '.m' or sp[1] == '.swift' or sp[1] == '.py':
                    print(i)
                    if i in g_filenames:
                        continue
                    with open(subPath,'r',encoding='utf-8') as f:
                      file =   f.readlines()
                      lines = len(file)
                      g_filenames.append(i)
                      g_lines.append(lines)


if __name__ == "__main__":
    analyse(currentPath)
    df = pd.DataFrame()
    df['file'] = g_filenames
    df['lines'] = g_lines
    df = df.sort_values(by='lines',ascending=False)
    topCount = 8
    if df.shape[0] < topCount:
        topCount = df.shape[0]

    topDf = df[:topCount]
    indexs = np.arange(len(topDf['file']))
    topDf = topDf.set_index(indexs+1)
    print(topDf)
    fig = plt.figure(figsize=(12,6))
    ax = fig.add_subplot(111)
    ax.set_ylabel('lines')
    ax.set_xlabel('files')
    ax.set_xticks(indexs)
    ax.set_xticklabels(topDf['file'])
    ax.grid(True)
    plt.bar(indexs,topDf['lines'],width=0.1,color='red')
    # plt.plot(topDf,kind='bar')
    plt.show()
