import requests, pdb, pandas as pd
from bs4 import BeautifulSoup
import csv
st = pdb.set_trace

outfile = 'ds_cur_items.txt'

html = open('./README.md', 'r').read()
#soup = BeautifulSoup(html, 'html.parser')

df = pd.read_html(html)[0]
df.drop(df.columns[0], axis=1, inplace=True)
dfl = df.values.tolist()

mods = ''
for week in dfl[:10]:
    mods += week[0]

items = mods.split('•')
nitems = []

for item in items:
    head, part, tail = item.partition('Total: ')
    nitems.append(head)

f = open(outfile, 'w')
for i in items:
    head, part, tail = i.partition('Total: ')
    f.write(i)
    f.write('\n')
f.close()







st()
