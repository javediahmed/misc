import os, sys
"""
Prints out files through subdirectories of base_path
with to files_{ext}.txt.
Args: first = T/F for include root, rest=file extension
      types ie .ipynb .py .txt etc.
Produces output file in current directory
"""

def findfiles(ext='.ipynb', base_path=os.getcwd(),
               outfile='', print_root=True, print_files=True):
    if not outfile:
        outfile = 'files_' + ext + '.txt'
    print(f'Looking for {ext} files in {base_path}') 
    print(f'Writing output file {outfile}')
    if print_files:
        print(f'\n Files found:')
    f = open(outfile,'w')
    for root, dirs, files in os.walk(base_path):
        for filename in files:
            if ext.lower() in filename.lower():
                if not print_root:
                    fileline = filename
                else: 
                    fileline = os.path.join(root, filename)
                f.write(fileline)
                f.write('\n')
                if print_files:
                    print(fileline)
    f.close()

if __name__=='__main__':
    # Default types to print
    args = ['.ipynb']
    print_root = True
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == 'f':
            print_root = False
            if len(sys.argv) > 2:
                args = sys.argv[2:]
        else:
            args = list(sys.argv[1:])
    #breakpoint()
    print(f"Looking for {args} in: {os.getcwd()}")
    for arg in args:
        findfiles(ext=arg, print_root=print_root)
