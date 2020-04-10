import os, pdb, pandas as pd, string

def printfiles(ext, filepath, outfile):
    flist = []
    dlist = []
    f = open(outfile,'w')
    for root, dirs, files in os.walk(filepath):
        for filename in files:
            if filename.endswith(ext):
                flist.append(filename)
                dlist.append(dirs)
                f.write(os.path.join(root,filename))
                f.write('\n')
                print(root)
                print(os.path.join(root, filename)) 
    f.close()
    
curpath = os.getcwd()
printfiles('.ipynb', curpath, 'files_ipynb.txt')
printfiles('.py', curpath, 'files_py.txt')
