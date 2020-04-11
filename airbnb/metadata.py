"""
Run download.py first
"""
import glob, pandas as pd, os, platform, pickle

outfile = 'metadata.pkl'

def get_metadata(filetype):
    target_files =  glob.glob(filetype)
    error_files = []
    meta = pd.DataFrame(columns=['country', 'state', 'city',
                                 'date', 'prefix', 'name', 'fullname'])
    for fname in target_files:
        meta_items = fname.split('_') + [fname]
        if len(meta_items) == len(meta.columns):
            meta.loc[len(meta)] = fname.split('_') + [fname]
        else:
            error_files.append(fname)
    meta['filename'] = meta.prefix + '_' + meta.name
    meta.drop(columns=['prefix', 'name'], inplace=True)
    return(meta, error_files)

def get_file_lists(meta_file):
    file_lists = []
    file_types = list(meta_file.filename.unique())
    files = list(meta_file.fullname.unique())
    for file_type in file_types:
        file_lists.append([f for f in files if file_type in f])
    return(file_lists)

if platform.node()[:3] == 'EC2':
    data_path = 'Y:/Dropbox/aws/data/' 
else:
    data_path = 'C:/files/metis/misc/airbnb/data'

def main():
    os.chdir(data_path)
    csv_files, csv_errors = get_metadata("*csv*")
    csv_lists = get_file_lists(csv_files)
    json_files, json_errors = get_metadata("*json*")
    json_lists = get_file_lists(json_files)
    pickle.dump((csv_files, csv_errors, csv_lists, json_files, json_errors, json_lists), open(outfile, 'wb'))

if __name__=='__main__':
    main()
