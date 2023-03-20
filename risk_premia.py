import pandas as pd
import numpy as np
import statsmodels.api as sm

def calculate_risk_premia(asset_returns, market_returns, rf_returns):
    """
    Calculate the risk premia for a given asset using the CAPM model.
    
    Parameters:
    asset_returns (pandas.Series): A series of returns for the asset.
    market_returns (pandas.Series): A series of returns for the market.
    rf_returns (pandas.Series): A series of returns for the risk-free asset.
    
    Returns:
    float: The calculated risk premia.
    """
    excess_market_returns = market_returns - rf_returns
    excess_asset_returns = asset_returns - rf_returns
    
    # Calculate beta
    X = sm.add_constant(excess_market_returns)
    model = sm.OLS(excess_asset_returns, X)
    results = model.fit()
    beta = results.params[1]
    
    # Calculate the risk premia
    risk_premia = beta * excess_market_returns.mean()
    
    return risk_premia
