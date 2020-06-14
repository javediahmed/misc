# Define the ticker list
import pandas as pd
tickers_list = ['AAPL', 'WMT', 'IBM', 'MU', 'BA', 'AXP']
# Import pandas
data = pd.DataFrame(columns=tickers_list)
# Fetch the data
import yfinance as yf
for ticker in tickers_list:
# data[ticker] = yf.download(ticker, "2015–01–01", "2019–01–01")['Adj Close']
 data[ticker] = yf.download(ticker, start="2017-01-01", end="2017-04-30")
#                   group_by="ticker")

# Print first 5 rows of the data
data.head()

# Plot all the close prices
((data.pct_change()+1).cumprod()).plot(figsize=(10, 7))
# Show the legend
plt.legend()
# Define the label for the title of the figure
plt.title('Adjusted Close Price', fontsize=16)
# Define the labels for x-axis and y-axis
plt.ylabel('Price', fontsize=14)
plt.xlabel('Year', fontsize=14)
# Plot the grid lines
plt.grid(which='major', color='k', linestyle='-.', linewidth=0.5)
plt.show()

