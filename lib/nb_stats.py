import json, sys, os
import itertools as it

def loc(nb):
    code_cells = [c for c in json.load(open(nb))['cells'] if c['cell_type'] == 'code']
    vals = list(map(sum, zip(*((1,len(c['source'])) for c in code_cells))))
    print(nb, vals)
    return vals

def run(ipynb_files):
    vals = list(map(sum, zip(*(loc(nb) for nb in ipynb_files))))
    print('totals:', vals)

notebooks = [f for f in os.listdir() if f.endswith('.ipynb') and not f.startswith('~')]
run(notebooks)
   

