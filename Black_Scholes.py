import numpy as np
from scipy.stats import norm

Phi = norm.cdf #Define Phi as Noramlized CDF
deriv_Phi = norm.pdf #Define Phi' as Normalized PDF

def black_scholes_call_price(vol, time_to_expiry, strike_price, current_price, risk_free): #Black Scholes call option price formula
    d_1 = 1/vol * 1/np.sqrt(time_to_expiry) * (np.log(current_price/strike_price) + (risk_free + vol**2/2) * time_to_expiry)
    d_2 = d_1 - vol * np.sqrt(time_to_expiry)
    term_1 = current_price * Phi(d_1)
    term_2 = strike_price * np.exp(-risk_free * time_to_expiry) * Phi(d_2)
    return term_1 - term_2

def black_scholes_put_price(vol, time_to_expiry, strike_price, current_price, risk_free): #Black Scholes put option price formula
    d_1 = 1/vol * 1/np.sqrt(time_to_expiry) * (np.log(current_price/strike_price) + (risk_free + vol**2/2) * time_to_expiry)
    d_2 = d_1 - vol * np.sqrt(time_to_expiry)
    return strike_price * Phi(-d_2) * np.exp(-risk_free * time_to_expiry) - current_price * Phi(-d_1)

"""# Test implementation
vol = np.array([0.1,0.55,1,2.5]) #0.55 here corresponds to 55% volatility
time_to_expiry = np.array([5,4,3,2]) # in years
strike_price = np.array([20,22.5,25,27.5]) # £ or $
current_price = 10 # $ or £
risk_free = 0.04 # 0.04 corresponds to 4% per year

prices = black_scholes_put_price(vol, time_to_expiry, strike_price, current_price, risk_free)
#print(prices)"""



def black_scholes_derivative(vol, time_to_expiry, strike_price, current_price, risk_free):
    d_1 = 1/vol * 1/np.sqrt(time_to_expiry) * (np.log(current_price/strike_price) + (risk_free + vol**2/2) * time_to_expiry)
    derivative = current_price * deriv_Phi(d_1) * np.sqrt(time_to_expiry)
    return(derivative)
"""derivs = black_scholes_derivative(vol, time_to_expiry, strike_price, current_price, risk_free)
print(derivs)"""
