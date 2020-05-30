import numpy as np, pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
import statsmodels.api as sm

results = []
n_rows = 20
n_train = 10
np.random.state = 4
noint = False

cats = ['Blue', 'Green', 'Red']
cats2 = ['Pink', 'Yellow', 'Purple']

df = pd.DataFrame(columns=['int', 'x1', 'x2', 'x3', 'y'])

df['int'] = np.ones(n_rows).astype(int)
df['x1'] = np.random.rand(n_rows)
df['x2'] = [np.random.choice(cats) for i in range(n_rows)]
df['x2'] = df['x2'].astype('category')
df['x3'] = [np.random.choice(cats2) for i in range(n_rows)]
df['x3'] = df['x3'].astype('category')
df['y'] = np.random.rand(n_rows)
ohc = OneHotEncoder()

x2_oh = pd.DataFrame(ohc.fit_transform(np.array(df['x2']).reshape(-1,1)).todense(), columns=['x2_' + i for i in cats]).astype('int')
x3_oh = pd.DataFrame(ohc.fit_transform(np.array(df['x3']).reshape(-1,1)).todense(), columns=['x3_' + i for i in cats2]).astype('int')

df = pd.concat([df.drop(columns='y'), x2_oh, x3_oh, df.y], axis=1).drop(columns=['x2', 'x3'])


if noint:
    df = df.drop(columns=['int'])

def regfit(dfn):
    X_train = dfn.iloc[:n_train, :-1]
    y_train = dfn['y'][:n_train]
    X_test = dfn.iloc[n_train:, :-1]
    y_test = dfn['y'][n_train:]
    lr = LinearRegression(fit_intercept=False)
    lrfit = lr.fit(X_train, y_train)
    return(lrfit, [X_train, y_train, X_test, y_test], 
           dict(zip(X_train.columns, np.round(lrfit.coef_, 3))))


lrfit, lrdata, lrcoef = regfit(df)

X_train, y_train, X_test, y_test = lrdata

results.append(res_blue)
results.append(res_red)

sm_reg = sm.OLS(y_train, X_train)
sm_result = ols.fit()

sm_result.params    
sm_result.summary()


a = lr_blue.predict(data_blue[2])
b = lr_red.predict(data_red[2])
c = np.round(a - b, 8).sum()
d = len(np.round(a - b, 8))

print(c/d)
print(results[0], '\n', results[1])

lr_blue.intercept_ + results[0]['x3_Red'] + results[0]['x3_Green']
lr_red.intercept_ + results[1]['x3_Blue'] + results[0]['x3_Green']

lr_blue.coef_
lr_red.coef_

xpx = np.dot(X_train.transpose(), X_train)
xpxi = np.linalg.inv(xpx)
xpy = np.dot(X_train.transpose(), y_train)
res = np.dot(xpxi, xpy)

xpx = X_train.T @ X_train
xpxi = np.linalg.inv(xpx)
xpy = X_train.T @ y_train
res = xpxi @ xpy





