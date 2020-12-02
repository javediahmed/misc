from fredapi import Fred
import matplotlib.pyplot as plt

fred=Fred(api_key_file='./f_api.txt')

data = fred.get_series('SP500')

print(data.head())

<<<<<<< HEAD:fred/python/test.py
#breakpoint()
=======
plt.plot(data)
plt.show()

breakpoint()
>>>>>>> 36121a5cdbf1f7fee7c77a35d0e9bc083eea000a:fred/python/misc/test.py


plt.plot(data)
plt.show()
