from brents_method import brent_method
from Get_options_data import get_options_data
from scipy.interpolate import LinearNDInterpolator
from scipy.interpolate import CloughTocher2DInterpolator
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import Black_Scholes as bs
import pandas as pd
import os
import datetime


def BS_brent_method(time_to_expiry, strike_price, current_price, risk_free, a, b, target_value, tol_height, tol_width, call):
    """Application of brent method to find implied volatility corresponding to that call/put price"""
    if target_value == 0:
        return("Error: price is 0")
    if call:
        def FUN(x):
            return bs.black_scholes_call_price(x,time_to_expiry, strike_price, current_price, risk_free)
    else:
        def FUN(x):
            return bs.black_scholes_put_price(x,time_to_expiry, strike_price, current_price, risk_free)
    return brent_method(FUN, a,b,target_value, tol_height, tol_width)


def get_vol_surface_data(ticker, tol_height = 0.001, tol_width = 0.001):
    """Find the data frames to plot the volatility surface """
    ticker_options_df = get_options_data(ticker)

    #If both bid and ask price exist use their average else use most recent price
    midpoint = 0.5 * (ticker_options_df["bid"] + ticker_options_df["ask"])
    prices = [x if x != 0 else y for x,y in zip(midpoint, ticker_options_df["lastPrice"])]
    ticker_options_df["Average_price"] = prices

    yf_ticker = yf.Ticker(ticker)
    yf_ticker_data = yf_ticker.history()
    last_quoted_price = yf_ticker_data["Close"].iloc[-1] # gets the last close data.

    init_lower = 0.001
    init_upper = 100
    risk_free = 0.049 #Risk free interest rate as 4.9%
    
    ticker_options_df = ticker_options_df[ticker_options_df["DTE"]!=0]
    option_prices = ticker_options_df[["Average_price"]].to_numpy()
    strikes = ticker_options_df[["strike"]].to_numpy()
    DTEs = ticker_options_df[["DTE"]].to_numpy()
    yfin_IVs = ticker_options_df[["impliedVolatility"]].to_numpy()
    calls = ticker_options_df[["call"]].to_numpy()
    
    #Calculate implied volatilities using Brents Algoritm and Black Scholes Equaiton
    IVs = [BS_brent_method(days_to_expiry/365, strike_price, last_quoted_price,risk_free, 
                       init_lower, init_upper, option_price, tol_height=tol_height, tol_width=tol_width, call= call)
                       for days_to_expiry, strike_price, option_price, call in zip(DTEs, strikes, option_prices, calls)]
    
    valid_indices = [not isinstance(iv, str) for iv in IVs]
    valid_IVs = [iv for iv in IVs if not isinstance(iv,str)]
    valid_IVs = np.squeeze(np.array(valid_IVs))
    valid_strikes = np.squeeze(strikes[valid_indices])
    valid_DTEs = np.squeeze(DTEs[valid_indices])
    valid_yfin_IVs = np.squeeze(yfin_IVs[valid_indices])
    valid_prices = np.squeeze(option_prices[valid_indices])

    valid_options = pd.DataFrame({"strike":valid_strikes,
                              "DTE":valid_DTEs,
                              "IV":valid_IVs, 
                              "yfin_IV":valid_yfin_IVs, 
                              "price": valid_prices})
    valid_options = valid_options.dropna(subset=["IV"]) 
    return(valid_options)

def plot(valid_options):
    """Plot Volatility Surface"""
    x = valid_options["strike"]
    y = valid_options["DTE"]
    z = valid_options["IV"]
    cmap = plt.get_cmap("viridis")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(x, y, z, c=z, cmap=cmap, s=5, marker='o')
    cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
    cbar.set_label('IV')
    ax.set_xlabel('Strike')
    ax.set_ylabel('DTE')
    ax.set_zlabel('IV')
    ax.set_title('3D Scatter Plot')
    ax.set_title('3D Scatter Plot')
    plt.show()

def save_to_csv(valid_options):
    """Save option details to CSV file"""
    file_path = os.path.abspath("")
    file_name = f"//{ticker}_data_on_{datetime.datetime.today().strftime('%Y-%m-%d')}.csv"
    valid_options.to_csv(file_path+file_name)

def lin_inter(valid_options):
    """Perform linear interpolation"""
    valid_options.sort_values(by=["strike","DTE"],inplace=True)
    plotted_options = valid_options.tail(-1)
    lin_interpolator = LinearNDInterpolator(list(zip(plotted_options["strike"],plotted_options["DTE"])), plotted_options["IV"])
    strike_vec = np.linspace(min(plotted_options["strike"]), max(plotted_options["strike"]))
    DTE_vec = np.linspace(min(plotted_options["DTE"]), max(plotted_options["DTE"]))
    X,Y = np.meshgrid(strike_vec,DTE_vec)
    IV_vals = lin_interpolator(X,Y)
    X_flat = X.flatten()
    Y_flat = Y.flatten()
    IV_vals_flat = IV_vals.flatten()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(X_flat, Y_flat, IV_vals_flat, c=IV_vals_flat, cmap="viridis", marker="o")
    fig.colorbar(scatter, ax=ax, label="Implied Volatility (IV)")
    plt.show()

def cubic_inter(valid_options):
    """Perform Cubit Interpolation"""

    valid_options.sort_values(by=["strike", "DTE"], inplace=True)
    plotted_options = valid_options.tail(-1)

    cubic_interpolator = CloughTocher2DInterpolator(
        list(zip(plotted_options["strike"], plotted_options["DTE"])), 
        plotted_options["IV"]
    )
    

    strike_vec = np.linspace(min(plotted_options["strike"]), max(plotted_options["strike"]))
    DTE_vec = np.linspace(min(plotted_options["DTE"]), max(plotted_options["DTE"]))
    X, Y = np.meshgrid(strike_vec, DTE_vec)
    
    IV_vals = cubic_interpolator(X, Y)
    
    X_flat = X.flatten()
    Y_flat = Y.flatten()
    IV_vals_flat = IV_vals.flatten()
    

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    

    scatter = ax.scatter(X_flat, Y_flat, IV_vals_flat, c=-IV_vals_flat, cmap='RdBu', marker='o')
    

    fig.colorbar(scatter, ax=ax, label='Implied Volatility (IV)')
    
    # Set axis labels and title
    ax.set_xlabel('Strike')
    ax.set_ylabel('DTE')
    ax.set_zlabel('Implied Volatility')
    ax.set_title('3D Scatter Plot of Interpolated IV Values')

    # Display the plot
    plt.show()


ticker = "META"
valid_options = get_vol_surface_data(ticker)
plot(valid_options)
lin_inter(valid_options)
cubic_inter(valid_options)



