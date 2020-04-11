"""
Run download.py, metadata.py first
"""

import glob, pandas as pd, os, pickle
from metadata import outfile as infile, data_path

csv_files, csv_errors, csv_lists, json_files, json_errors, json_lists = pickle.load(open(data_path + infile, 'rb'))
us_files = csv_files[csv_files.country == 'united-states']
us_calendar_files = [x for x in csv_lists[0] if 'united-states' in x]

us_calendar_data = csv_files[[i in us_calendar_files for i in csv_files.fullname]]

usefile = 'united-states_ny_new-york-city_2015-01-01_data_calendar.csv.gz'

from readdata 

breakpoint()
