import yfinance as yf
from matplotlib import pyplot as plt
from pdb import set_trace as st
data = yf.download("SPY AAPL", start="2017-01-01", end="2017-04-30",
                   group_by="ticker")


st()


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
