import numpy as np
from scipy.stats import norm

def replication(S, K, r, t, sigma, option_type):
    """
    Calculate the option replication parameters using the Black-Scholes model.
    
    Parameters:
    S (float): underlying asset price
    K (float): option strike price
    r (float): risk-free interest rate
    t (float): time to option expiration (in years)
    sigma (float): underlying asset volatility
    option_type (str): option type, either 'call' or 'put'
    
    Returns:
    dict: a dictionary containing the option replication parameters:
        delta (float): the number of shares required to replicate the option
        gamma (float): the rate of change of delta with respect to the underlying asset price
        vega (float): the rate of change of the option value with respect to underlying asset volatility
        theta (float): the rate of change of the option value with respect to time to expiration
        rho (float): the rate of change of the option value with respect to the risk-free interest rate
    """
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*t) / (sigma*np.sqrt(t))
    d2 = d1 - sigma*np.sqrt(t)
    N = norm.cdf if option_type == 'call' else norm.cdf(-d1)
    N_prime = norm.pdf
    delta = N(d1)
    gamma = N_prime(d1) / (S*sigma*np.sqrt(t))
    vega = S * N_prime(d1) * np.sqrt(t)
    theta = - (S * N_prime(d1) * sigma) / (2*np.sqrt(t)) - r*K*np.exp(-r*t) * N(option_type == 'call' and d1 or -d1)
    rho = K*t*np.exp(-r*t) * N(option_type == 'call' and d2 or -d2)
    return {'delta': delta, 'gamma': gamma, 'vega': vega, 'theta': theta, 'rho': rho}
