import nbformat, sys, os, pdb
from nbconvert.preprocessors import ExecutePreprocessor
print(sys.argv[1])
notebook_filename = str(sys.argv[1])
nb = nbformat.read(open(notebook_filename), as_version=4)
ep = ExecutePreprocessor(timeout=600, kernal_name='metis')
ep.preprocess(nb, {'metadata': {'path': './'}})
