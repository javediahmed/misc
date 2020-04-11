
import numpy as np, pandas as pd
from matplotlib import pyplot as plt

data_path = 'data/'
infiles = ('turnstile_111022.txt', 'turnstile_151114.txt')

df1 = pd.read_csv(data_path + infiles[0], sep=',', header=None)
df2 = pd.read_csv(data_path + infiles[1], sep=',', header=0)

df2['time'] = pd.to_datetime(df2.DATE + ';' + df2.TIME)



dg = df2.groupby(['time'])['ENTRIES'].sum()

breakpoint()
