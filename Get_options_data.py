import yfinance as yf
import pandas as pd
import datetime

def get_options_data(ticker):
    """Function finds list of all options chains for all the available options for a stock
    Ticker is a string of the stock for which the option chain is being found
    ticker = string
    output = pandas concated dataframe of put and call options for all expiry dates"""
    ticker = yf.Ticker(ticker) #Converts input ticker string to a ticker object
    expiry_dates = ticker.options #Get list of expiration dates for stocks 
    options_data = pd.DataFrame() #Create an empty dataframe to store all option chains
    for expiry in expiry_dates:
        current_option_chain = ticker.option_chain(expiry)
        call_df = current_option_chain.calls
        put_df = current_option_chain.puts
        call_df["call"] = True #Create a column to distinguish between call and put options
        put_df["call"] = False
        # Reformatting it to be a single data frame:
        current_option_chain = pd.concat([call_df, put_df])
        current_option_chain["Expiration"] = pd.to_datetime(expiry)
        options_data = pd.concat([options_data, current_option_chain])
    
    options_data["DTE"] = (options_data["Expiration"] - datetime.datetime.today()).dt.days
    options_data = options_data.drop(columns = ["contractSize","currency","percentChange"])
    return options_data
