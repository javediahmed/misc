import glob, pandas as pd

file_list = glob.glob("*data_calendar*")

dfs, names, errors = [], [], []
data = pd.DataFrame()
for filename in file_list[:5]:
    print(filename)
    names.append(filename)
    try:
        df = pd.read_csv(filename, compression='gzip')
        df['price'] = df['price'].str.replace('$', '')
        df['price'] = df['price'].str.replace(',', '')
        df['price'] = df['price'].astype(float)
        df['available'] = df.available == 't'
        dfs.append(df)
        data = pd.concat([data, df])
    except EOFError:
        errors.append(filename)
        
dft = dfs[0].groupby('date').agg('mean')



