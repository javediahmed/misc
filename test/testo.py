import requests, pdb, pandas as pd
from bs4 import BeautifulSoup
import csv
st = pdb.set_trace

outfile = 'ds_cur_items.txt'

html = open('/Users/javed/metis/dscurriculum_c1/README.md', 'r').read()
#soup = BeautifulSoup(html, 'html.parser')

df = pd.read_html(html)[0]
df.drop(df.columns[0], axis=1, inplace=True)
dfl = df.values.tolist()

st()

f = open(outfile, 'w')

for i in dfl[0]:
    print(i)
    print(type(i))
    for j in i[0]:
        print(j)




# mods = ''
# for week in dfl[:10]:
#     mods += week[0]

# items = mods.split('•')
# nitems = []

# st()

# for item in items:
#     head, part, tail = item.partition('Total: ')
#     nitems.append(head)

# for i in items:
#     head, part, tail = i.partition('Total: ')
#     f.write(i)
#     f.write('\n')
# f.close()







st()
