from alpaca.trading.client import TradingClient

import alpaca_trade_api as tradeapi


from MSOAI import StockSummary, StockInfo

from dotenv import load_dotenv
import os

# from trading_classes import get_asset_info

from yahooquery import Screener

import pandas as pd
import matplotlib.pyplot as plt 



# This primarily to test my algorithim by adding into my Paper Traeding Simulator

# Load our env files
load_dotenv()


ALPACA = os.getenv('ALPACA')


SECRET_KEY = os.getenv('SECRET_KEY')



# This is my account for experimental stuff such as using paper trading in order
# to experiment with my algorithims
trading_client = TradingClient(api_key=ALPACA, secret_key=SECRET_KEY)

# This is the main api
trading_api = tradeapi.REST(key_id=ALPACA, secret_key=SECRET_KEY)





account = trading_client.get_account()

print(type(account))



# print(get_asset_info)


def get_losers():
    info = Screener()
    losers = info.get_screeners('day_losers')  # Returns dict



    quotas = losers['day_losers']['quotes']

    # List of losers (Harsh haha): We shall append it
    losers = []
    #  We want to iterate and grab the values of the day losers: Company, ticker, and its drop in price
    for item in quotas:
        company = item.get('shortName')
        ticker = item.get('symbol')
        daily_loss = item.get('regularMarketChangePercent')
        losers.append((company, ticker, daily_loss))
    return losers

def graph_losers():
    N = 10
    losers_information = get_losers()[:N] # LIMIT OF 10
    

    
    # Label
    ticker = [item[1] for item in losers_information]
    loss_daily = [item[2] for item in losers_information]



    for tick, loss in (zip(ticker, loss_daily)):
        print(tick, loss)
        

    
    # Top 10 losers:

    
    
    plt.figure(figsize=(10,6))




graph_losers()