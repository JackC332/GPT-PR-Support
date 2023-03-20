import pandas as pd
from mibian import BlackScholes

class OptionStrategy:
    def __init__(self, underlying_price, options):
        self.underlying_price = underlying_price
        self.options = options
        self.df = pd.DataFrame(self.options)
        self.df['price'] = self.df.apply(
            lambda x: BlackScholes(
                x['underlying_price'],
                x['strike_price'],
                x['interest_rate'],
                x['days_to_expiry'],
                x['option_type'],
                x['volatility']
            ).callPrice if x['option_type'] == 'C' else BlackScholes(
                x['underlying_price'],
                x['strike_price'],
                x['interest_rate'],
                x['days_to_expiry'],
                x['option_type'],
                x['volatility']
            ).putPrice,
            axis=1
        )
    
    def get_profit(self, underlying_price):
        self.df['underlying_price'] = underlying_price
        calls = self.df[self.df['option_type'] == 'C']
        puts = self.df[self.df['option_type'] == 'P']
        return calls[calls['strike_price'] < underlying_price]['price'].sum() - \
            calls[calls['strike_price'] > underlying_price]['price'].sum() + \
            puts[puts['strike_price'] < underlying_price]['price'].sum() - \
            puts[puts['strike_price'] > underlying_price]['price'].sum()

