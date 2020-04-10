import pandas as pd

readme_path = '/Users/javed/metis/dscurriculum_c1/'
readme_file = 'README.md'
outpath = '/Users/javed/metis/lib/misc/'
outfile = 'ds_cur_items.txt'

html = open(readme_path + readme_file, 'r').read()
df = pd.read_html(html)[0]

df[df.isna()] = 'NA'
days = df.columns[1:].tolist()
df.columns = ['Week'] + days
dfl = df.values.tolist()

mods = []
for i in range(len(dfl)):
    mods += sum([x.split('•') for x in dfl[i]], [])

mods = [i.strip() for i in mods if i[:3] not in('Tot', 'Wee', 'NA')]

f = open(outpath + outfile, 'w')
for i in mods:
    f.write(i)
    f.write('\n')
f.close()
