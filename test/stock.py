from yahoo_historical import Fetcher as f
from pdb import set_trace as st
from matplotlib import pyplot as plt
import numpy as np, pandas as pd
from statsmodels.tsa.arima_model import ARIMA
from  statsmodels.tsa.seasonal import seasonal_decompose as seasonal_decompose

tickers = ["AAPL", "MSFT"]
data_start = [2007,1,1]
data_end = [2018,12,31]


#s_data = f("AAPL",[2007,1,1],[2018,12,31])
#s_hist = s_data.getHistorical()
#s_list = [f(x, data_start, data_end) for x in tickers]

s1 = f(tickers[0], data_start, data_end)
df1 = s1.getHistorical()


df1['Ticker'] = s1.ticker
df1 = df1.merge(s1.getDividends(), how='left', on='Date').fillna(0)
df1['ret'] = df1.Close / df1.Close.shift(1) - 1
df1['retadj'] = df1['Adj Close'] / df1['Adj Close'].shift(1) - 1
df1['retdel'] = df1.ret - df1.retadj
df1['delta'] = df1['Close'] - df1['Adj Close']
df1['delta_p'] = (df1['Close'] - df1['Adj Close'])/df1.Close
df1['divyld'] = df1.Dividends / df1.Close
df1['Date'] = pd.to_datetime(df1.Date).dt.normalize()
#df1.set_index('Date', inplace=True)
df1['cumdiv'] = df1.Dividends.cumsum()
dft = df1[['Close', 'Adj Close', 'Dividends', 'delta', 'delta_p', 'cumdiv']]


##################################
# Forecast params
ds = df1.iloc[:,:3]
min_days = 50
fcst_days = 30
fcst_start = min(ds.index) + min_days
num_fcsts = len(ds[df1.index > fcst_start])


nresult = seasonal_decompose(df1 - np.mean(df1), model='additive', freq=20)

nresult.plot()


sns.lineplot(ds, time='Date', value='Open')



st()

for i in range(min_days, num_fcsts):
    hist = ds.iloc[:,1:]
    acts = ds.iloc[i:fcst_days+i,1:]
    pred = pd.DataFrame()
    for j in hist.columns:
        model = ARIMA(hist[j], order=(1, 0, 1))
        mfit = model.fit(disp=False)
        pred[j] = mfit.predict(i, i + fcst_days)

st()

    
    

