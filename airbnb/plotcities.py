"""
Run download.py, metadata.py first
"""

import glob, pandas as pd, os, pickle, matplotlib.pyplot as plt, numpy as np


DATA_PATH = './data/'
OUTPATH = './output/'
CITIES = ('seattle', 'los-angeles', 'washington', 'san-francisco')
#CITIES = ('seattle',)
NUM_LINES = 4

def combine(file_list, maxdays = 360):
    dfs, names = [], []
    for filen in file_list:
        newdf = pd.read_pickle(filen)
        stamp = str(newdf.index[0].date())
        newdf.columns = ['_'.join(col).strip() for col in newdf.columns.values]
        newdf['stamp'] = stamp
        newdf['stampdate'] = pd.to_datetime(newdf['stamp'])
        newdf = newdf[newdf.index - newdf.stampdate < np.timedelta64(maxdays, 'D')]
        dfs.append(newdf.drop(columns='stampdate'))
    return dfs

def main():
    curdir = os.getcwd()
    print(f'Current directory: {curdir}') 
    for city in CITIES:
        readfiles = glob.glob(DATA_PATH + f'*{city}*agg.pkl')
        print(f'{len(readfiles)} files found for {city}')
        dfs = combine(readfiles)
        alldata = pd.concat(dfs[2:])
        allwide = alldata.reset_index().set_index(['date','stamp']).unstack()
#        print(allwide.head())
#        breakpoint()
        pldata = pd.concat([i[5:-1] for i in dfs[-NUM_LINES:]])
#        breakpoint()
        plwide = pldata.reset_index().set_index(['date','stamp']).unstack()
        plwide.rolling(1).mean().available_mean.plot(figsize=(20, 20), linewidth=3)
        print(f'Saving plots for {city}')
        plt.savefig(OUTPATH + f'{city}_avail.png')
        plwide.rolling(7).mean().available_mean.plot(figsize=(20, 20), linewidth=3)
        plt.savefig(OUTPATH + f'{city}_avail_roll7.png')
        plwide.rolling(1).mean().price_mean.plot(figsize=(20, 20), linewidth=3)
        plt.savefig(OUTPATH + f'{city}_price.png')
        plwide.rolling(7).mean().price_mean.plot(figsize=(20, 20), linewidth=3)
        plt.savefig(OUTPATH + f'{city}_price_roll7.png')
    
if __name__=='__main__':
    main()
