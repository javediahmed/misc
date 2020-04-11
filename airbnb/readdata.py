"""
Run download.py, metadata.py first
"""

import glob, pandas as pd, os, pickle
from metadata import outfile as infile, data_path
outfile = 'us_df.pkl'
outfile_test = 'us_df_int.pkl'
error_file = 'errors.pkl'

def read_files(file_list):
    errors, output_df = [], pd.DataFrame()
    for fname in file_list:
        print(fname)
        try:
            df = pd.read_csv(fname)
            df['fullname'] = fname
            output_df = pd.concat([output_df, df])
        except EOFError:
            errors.append(fname)
    return output_df.drop_duplicates(), errors

def read_calendar_file(fname, dpath=data_path):
    print(fname)
    df = pd.read_csv(dpath + fname)
    df['fullname'] = fname
    df['price'] = df['price'].str.replace('$', '')
    df['price'] = df['price'].str.replace(',', '')
    df['price'] = df['price'].astype(float)
    df['available'] = df.available == 't'
    return df

lists = pickle.load(open(data_path + infile, 'rb'))
csv_files, csv_errors, csv_lists, json_files, json_errors, json_lists = lists
us_files = csv_files[csv_files.country == 'united-states']
us_calendar_files = [x for x in csv_lists[0] if 'united-states' in x]
us_calendar_data = csv_files[[i in us_calendar_files for i in csv_files.fullname]]

if __name__=='__main__':
    dfs, errors = [], []
    for i, fname in enumerate(us_calendar_files):
        try:
            dfs.append(read_calendar_file(fname))
        except:
            errors.append(fname)
        if i % 100 == 0:
            pickle.dump(dfs, open(data_path + outfile_test, 'wb'))
    df_us = pd.concat(dfs)
    df_us.to_pickle(data_path + outfile)
    pickle.dump(errors, open(error_file, 'wb'))
