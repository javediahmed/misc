"""
Run download.py, metadata.py first
"""

import glob, pandas as pd, os, pickle
from metadata import outfile as infile, data_path
outfile = 'us_df.pkl'
outfile_test = 'us_df_int.pkl'
error_file = 'errors.pkl'

def agg_calendar_file(df, datevar='date', idvar='listing_id'):
    df.groupby('date')

def read_calendar_file(fname, dpath=data_path, agg=False, output=False):
    print(fname)
    df = pd.read_csv(dpath + fname)
    df['fullname'] = fname
    df['available'] = df.available == 't'
    df['price'] = df['price'].str.replace('$', '')
    df['price'] = df['price'].str.replace(',', '')
    df['price'] = df['price'].astype(float)
    df['date'] = pd.to_datetime(df['date'])
    if 'adjusted_price' in df.columns:
        df['adjusted_price'] = df['adjusted_price'].str.replace('$', '')
        df['adjusted_price'] = df['adjusted_price'].str.replace(',', '')
        df['adjusted_price'] = df['adjusted_price'].astype(float)  

    if output:
        if agg:
            output_name = dpath + fname.split('.')[0] + '_agg' + '.pkl'
            mindate = df.date.min()
            df = df.groupby('date').agg({'available':['count', 'mean'], 'price':['count', 'mean']})
            print('Writing output file: ', output_name)
            df.to_pickle(output_name, protocol=4)
        else:    
            output_name = dpath + fname.split('.')[0] + '.pkl'
            print('Writing output file: ', output_name)
            df.to_pickle(output_name, protocol=4)
    return df

def read_files(file_list, output=False, output_file='test.pkl'):
    errors, output_df = [], pd.DataFrame()
    for fname in file_list:
        print(fname)
        try:
            df = pd.read_csv(fname)
            df['fullname'] = fname
            output_df = pd.concat([output_df, df])
        except EOFError:
            errors.append(fname)
    if output:
        print('Writing output file') 
        pickle.dump(output_df, open(output_file, 'wb'), protocol=4)        
    return output_df.drop_duplicates(), errors


lists = pickle.load(open(data_path + infile, 'rb'))
csv_files, csv_errors, csv_lists, json_files, json_errors, json_lists = lists
us_files = csv_files[csv_files.country == 'united-states']
us_calendar_files = [x for x in csv_lists[0] if 'united-states' in x]
us_calendar_data = csv_files[[i in us_calendar_files for i in csv_files.fullname]]
state_calendar_files, city_calendar_files = [], []
states = list(us_calendar_data.state.unique())
cities = list(us_calendar_data.city.unique())
for s in states:
    files = list(us_calendar_data[us_calendar_data.state == s]['fullname'])
    state_calendar_files.append(files)

for c in cities:
    files = list(us_calendar_data[us_calendar_data.city == c]['fullname'])
    city_calendar_files.append(files)

city_files_dict = dict(zip(cities, city_calendar_files))
   
def main():
    for fname in city_files_dict['seattle']:
#        read_calendar_file(fname, dpath=data_path, output=True)
        read_calendar_file(fname, dpath=data_path, output=True, agg=True)
    
if __name__=='__main__':
    main()




#cities ['los-angeles', 'oakland', 'pacific-grove', 'san-diego',
#       'san-francisco', 'san-mateo-county', 'santa-clara-county',
#       'santa-cruz-county', 'denver', 'washington-dc', 'broward-county',
#       'hawaii', 'chicago', 'new-orleans', 'boston', 'cambridge',
#       'twin-cities-msa', 'asheville', 'jersey-city', 'clark-county-nv',
#       'new-york-city', 'columbus', 'portland', 'salem-or',
#       'rhode-island', 'nashville', 'austin', 'seattle']
