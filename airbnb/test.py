"""
Run download.py, metadata.py first
"""

import glob, pandas as pd, os, pickle, matplotlib.pyplot as plt
from metadata import outfile as infile, data_path

curdir = os.getcwd()
os.chdir(data_path)

seafiles = glob.glob('*seattle*agg.pkl')
dfs = []
names = []
for sfile in seafiles:
    newdf = pd.read_pickle(sfile)
    stamp = str(newdf.index[0].date())
    newdf.columns = ['_'.join(col).strip() for col in newdf.columns.values]
    newdf['stamp'] = stamp
    dfs.append(newdf)
    names.append(stamp)

avail = pd.DataFrame(columns=names)


#breakpoint()
