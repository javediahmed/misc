import glob, pandas as pd, os, platform

def get_metadata(filetype):
    target_files =  glob.glob(filetype)
    meta = pd.DataFrame(columns=['country', 'state', 'city',
                                 'date', 'prefix', 'name', 'fullname'])
    for fname in target_files:
        meta.loc[len(meta)] = fname.split('_') + [fname]
    meta['filename'] = meta.prefix + '_' + meta.name
    meta.drop(columns=['prefix', 'name'], inplace=True)
    return(meta)

def get_file_lists(meta_file):
    file_lists = []
    file_types = list(meta_file.filename.unique())
    files = list(meta_file.fullname.unique())
    for file_type in file_types:
        file_lists.append([f for f in files if file_type in f])
    return(file_lists)

def read_files(file_list):
    errors, output_df = [], pd.DataFrame()
    for f in file_list:
        print(f)
        try:
            df = pd.read_csv(f)
            df['fullname'] = f
            output_df = pd.concat([output_df, df])
        except EOFError:
            errors.append(f)
    return output_df.drop_duplicates(), errors

if platform.node()[:3] == 'EC2':
    data_path = 'Y:/Dropbox/aws/data/' 
else:
    data_path = 'C:/files/metis/misc/airbnb/data'
os.chdir(data_path)
csv_files = get_metadata("*csv*")
csv_lists = get_file_lists(csv_files)
json_files = get_metadata("*json*")
json_lists = get_file_lists(json_files)
df, errors = read_files(csv_lists[0])
df['price'] = df['price'].str.replace('$', '')
df['price'] = df['price'].str.replace(',', '')
df['price'] = df['price'].astype(float)
df['available'] = df.available == 't'
df.to_pickle(data_path + 'calendar.pkl')

