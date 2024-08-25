import yfinance as yf
import pandas as pd
import datetime

# Checking version of yfinance.
print(yf.__version__)

# Set up a yfinance Ticker object for a given ticker:
ticker = "AAPL"
aapl = yf.Ticker(ticker)

#Actions in Past Year
aapl.history(period = "1y")
aapl.actions

# To get metadata about the stock:
aapl.history_metadata

#Get data about the current major holders of the stock:
aapl.institutional_holders # major institutional holders

# Get recent news articles relating to the stock with .news
aapl.news

expiry_dates = aapl.options # Get expiry dates of AAPL options
print(expiry_dates[0]) #Return Earliest Expiry date

#Get option chain for the option at earliest expiry date
first_option_chain = aapl.option_chain(expiry_dates[0]) 

