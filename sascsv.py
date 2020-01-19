import pandas as pd
import sys, time
from pdb import set_trace as st
from sas7bdat import SAS7BDAT

start = time.time()

try:
    infile = sys.argv[1]
except IndexError:
    print("Specify file to convert")
    sys.exit(1)
try:
    outfile = sys.argv[2]
except IndexError:
    outfile = infile.split('.')[0] + '.csv'

print('Reading in: ', infile)
with SAS7BDAT(infile, skip_header=False) as reader:
    df = reader.to_data_frame()
print('Writing out: ', outfile)
df.to_csv(outfile)

end = time.time()

print('Time: ', round(end-start,2)/60, ' minutes')
