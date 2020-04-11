"""
Run download.py, metadata.py first
"""

import glob, pandas as pd, os, pickle, matplotlib.pyplot as plt
from metadata import outfile as infile, data_path

curdir = os.getcwd()
os.chdir(data_path)

seafiles = glob.glob('*seattle*agg.pkl')
dfs = []

for sfile in seafiles:
    dfs.append(pd.read_pickle(sfile))

#breakpoint()
