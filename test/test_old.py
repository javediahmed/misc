import pandas as pd

df1 = pd.read_csv('data.txt')
df2 = pd.read_csv('data.txt', header=0, sep=' ')
df3 = pd.read_csv('data.txt', delim_whitespace=True)
df4 = pd.read_csv('data.txt', header=None, delim_whitespace=True)
df5 = pd.read_csv('data.txt', delim_whitespace=True)

breakpoint()

