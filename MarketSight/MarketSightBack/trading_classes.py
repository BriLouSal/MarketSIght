import pandas as pd
import yfinance as yf
from tqdm import tqdm
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator
from ta.volatility import BollingerBands



# Obtain top loser from today's stock market
from yahooquery import Screener
import matplotlib.pyplot as plt 

from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockSnapshotRequest

import os
from dotenv import load_dotenv
import datetime


load_dotenv()

API_KEY = os.getenv('ALPACA')
SECRET_KEY = os.getenv('SECRET_KEY')


# ACTUALLY THE EARLY VERSION THAT IS NOW BULLISH INDICATOR ANG DAILY WINNER XD


def get_asset_info(self, df=None):
        """
        Description:
        Grabs historical prices for assets, calculates RSI and Bollinger Bands tech signals, and returns a df with all this data for the assets meeting the buy criteria.
        Argument(s):
            • df: a df can be provided to specify which assets you'd like info for since this method is used in the Alpaca class. If no df argument is passed then tickers from get_trading_opportunities() method are used.
        """

        # Grab technical stock info:
        if df is None:
            all_tickers = self.all_tickers
        else:
            all_tickers = list(df["yf_ticker"])

        df_tech = []
        for i, symbol in tqdm(
            enumerate(all_tickers),
            desc="• Grabbing technical metrics for "
            + str(len(all_tickers))
            + " assets",
        ):
            try:
                Ticker = yf.Ticker(symbol)
                Hist = Ticker.history(period="1y", interval="1d")

                for n in [14, 30, 50, 200]:
                    # Initialize MA Indicator
                    Hist["ma" + str(n)] = sma_indicator(
                        close=Hist["Close"], window=n, fillna=False
                    )
                    # Initialize RSI Indicator
                    Hist["rsi" + str(n)] = RSIIndicator(
                        close=Hist["Close"], window=n
                    ).rsi()
                    # Initialize Hi BB Indicator
                    Hist["bbhi" + str(n)] = BollingerBands(
                        close=Hist["Close"], window=n, window_dev=2
                    ).bollinger_hband_indicator()
                    # Initialize Lo BB Indicator
                    Hist["bblo" + str(n)] = BollingerBands(
                        close=Hist["Close"], window=n, window_dev=2
                    ).bollinger_lband_indicator()

                df_tech_temp = Hist.iloc[-1:, -16:].reset_index(drop=True)
                df_tech_temp.insert(0, "Symbol", Ticker.ticker)
                df_tech.append(df_tech_temp)
            except:
                KeyError
            pass

        df_tech = [x for x in df_tech if not x.empty]
        df_tech = pd.concat(df_tech)

        # Define the buy criteria
        buy_criteria = (
            (df_tech[["bblo14", "bblo30", "bblo50", "bblo200"]] == 1).any(axis=1)
        ) | ((df_tech[["rsi14", "rsi30", "rsi50", "rsi200"]] <= 30).any(axis=1))

        # Filter the DataFrame
        buy_filtered_df = df_tech[buy_criteria]

        # Create a list of tickers to trade
        self.buy_tickers = list(buy_filtered_df["Symbol"])

        return buy_filtered_df


# def get_losers():
#     info = Screener()
#     losers = info.get_screeners('day_losers')  # Returns dict



#     quotas = losers['day_losers']['quotes']

#     # List of losers (Harsh haha): We shall append it
#     losers = []
#     #  We want to iterate and grab the values of the day losers: Company, ticker, and its drop in price
#     for item in quotas:
#         company = item.get('shortName')
#         ticker = item.get('ticker')
#         daily_loss = item.get('regularMarketChangePercent')
#         losers.append((company, ticker, daily_loss))
#     return losers.sort()



# def graph(list_of_stocks: list):
#     for x in list_of_stocks:
#         stocks = pd.DataFrame(list_of_stocks,columns=['Company', "Ticker", "Daily % Loss"])
#         stocks_sorted = stocks.sort_values("Daily % Loss")

#         plt.figure(figsize=(10, 6))
#         plt.is_interactive()
    


# print(get_losers())



def rsi_strength(stock: str):
    stock = stock.upper()
    stock_info = yf.download(tickers=stock, period='6mo', interval='1d')

    if stock_info is None:
        return f"The stock: {stock} Does not exist. Please Try again or recheck"

    strength = RSIIndicator(close=stock_info['Close'], window=14)

    data = strength.rsi()

    print(data[["Close", "RSI"]].tail())

    plt.figure(figsize=(10,5))
    plt.plot(data["RSI"], label="RSI (14)")
    plt.axhline(70, color='red', linestyle='--')
    plt.axhline(30, color='green', linestyle='--')
    plt.title(F"RSI for {stock}")
    plt.legend()
    plt.show()

    

# THEORIZE, WE CAN USE PLOTS IN GRAPH TO DETERMINE BULLISH PATTERN, BEARISH PATTERN, ETC.



def get_losers():
    info = Screener()
    losers = info.get_screeners('day_losers')  # Returns dict



    quotas = losers['day_losers']['quotes']

    # List of losers (Harsh haha): We shall append it
    losers = []
    #  We want to iterate and grab the values of the day losers: Company, ticker, and its drop in price
    for item in quotas:
        company = item.get('shortName')
        ticker = item.get('ticker')
        daily_loss = item.get('regularMarketChangePercent')
        losers.append((company, ticker, daily_loss))
    return losers

# def getStockPrice(stock: str) -> float:
#     stock = stock.upper()
#     stock_client = StockHistoricalDataClient(API_KEY, SECRET_KEY)
#     stock_price = stock_client.get_stock_snapshot(StockSnapshotRequest(symbol_or_symbols=stock))
#     return stock_price.latest_trade.price



# print(getStockPrice(stock='AAPL'))