from fredapi import Fred

fred=Fred(api_key_file='./f_api.txt')

data = fred.get_series('SP500')

print(data.head())

breakpoint()

