from fredapi import Fred
import matplotlib.pyplot as plt

# Note -- need to have an access token stored in f_api.txt
fred=Fred(api_key_file='./f_api.txt')

data = fred.get_series('SP500')

print(data.head())

plt.plot(data)
plt.show()

