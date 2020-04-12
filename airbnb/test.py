"""
Run download.py, metadata.py first
"""

import glob, pandas as pd, os, pickle, matplotlib.pyplot as plt, numpy as np
from metadata import outfile as infile, data_path


curdir = os.getcwd()
curdir = 'Z:/files/misc/airbnb/'
os.chdir(data_path)

readfiles = glob.glob('*seattle*agg.pkl')

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

dfs = combine(readfiles)

alldata = pd.concat(dfs[2:])
allwide = alldata.reset_index().set_index(['date','stamp']).unstack()
pldata = pd.concat([i[5:-1] for i in dfs[20:]])
plwide = pldata.reset_index().set_index(['date','stamp']).unstack()
plwide.rolling(1).mean().available_mean.plot(figsize=(20, 20), linewidth=2)
plwide.rolling(7).mean().available_mean.plot(figsize=(20, 20), linewidth=2)
plwide.rolling(1).mean().price_mean.plot(figsize=(20, 20), linewidth=2)
plwide.rolling(7).mean().price_mean.plot(figsize=(20, 20), linewidth=2)



