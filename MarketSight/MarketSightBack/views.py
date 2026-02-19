
# Main Django library

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from decimal import Decimal
from django.db import transaction


# User authentication library from Django


from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
# Used for Performance
from django.core.cache import cache

from .backend import EmailBackend

# # Error checker
# import sys
# print(sys.executable)
# # email

from django.core.mail import send_mail
from django.conf import settings

# Investment Endeavors Library

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass, AssetStatus

from datetime import datetime, timedelta
from yahooquery import Ticker, search



from django.contrib import messages

import pandas as pd
import matplotlib.pyplot as pl





import markdown


from .models import Profile, Portfolio, StockOrder, StockPosition
# from alpaca.data.historical import CryptoHistoricalDataClient

from .MSOAI import (
    FinancialReport,
    Company_Analysis,
    Revenue_Analysis,
    Returns_Efficiency_Ratios,
    Growth_Analysis_Outlook,
    Growth_of_Stock,
    Company_Debt,
    StockInfo,
    html_to_paragraph_text,
    bullish,
    bullish_indicator,
    ETF_FinancialReport,
    is_etf

    
    
)
# Performance
from asgiref.sync import sync_to_async, async_to_sync
import asyncio
from django.core.cache import cache


# Stock backup (INCASE IT'S NEEDED FOR VIEWS.PY IN ORDER FOR IT TO BE SEAMLESS)
import yfinance as yf

import ta


import json
import os 
from dotenv import load_dotenv
from yahooquery import Screener




load_dotenv()




#  This is the views.py file where we will handle the logic for our application
#  We will create views for home, portfolio room, stock, login, signup, and assistance



#  This is a list of stocks that we will use to display in the portfolio room
ticker = []

# This will be used as a feature to store recent_search of a user stock
recent_search = {}

def capital_asset_pricing_models(ticker: str):
    stock = Ticker(symbols=ticker)
    # Grab the beta of the stock
    key_stats = stock.key_stats.get(ticker, {}) or {}
    beta = key_stats.get('beta', 1.0)

    treasury_ticker = Ticker("^TNX")
    # Grab risk_free_rate via treasury bonds, and also grab the beta of the stock.
    
    risk_free_rate = (treasury_ticker.history(period='1d')['close'].iloc[-1]) / 100

    # Grab expected market returns using SP500, and get its information
    index = Ticker('^GSPC')
    
    YEARS_SP500 = 10
    end_date = datetime.now()
    date_of_sp500 = end_date - timedelta(days=YEARS_SP500*365)

    
    # Use CAGR of SP500 to get the expected market return
    # Formula: (Ending Value / Beginning Value)^(1 / Number of Years) - 1

    # Get the sp500 value at beginning of the interval and ending via indexation

    history_of_index = index.history(start=date_of_sp500, end=end_date)


    ending_value = history_of_index['adjclose'].iloc[-1]
    start_value = history_of_index['adjclose'].iloc[0]


    market_return = ((ending_value / start_value) ** (1/ YEARS_SP500)) - 1

    # CAPM FORMULA: : Expected Return = Risk-Free Rate + Beta × (Expected Market Return - Risk-Free Rate

    return round((risk_free_rate + beta * (market_return -  risk_free_rate) * 100), 2)


def dailyWinners():


    s = Screener()
    stocks = s.get_screeners(['day_gainers'], count=5)
    gainers_list = stocks.get('day_gainers', {}).get('quotes', [])
    sorted_gainers = sorted(
        gainers_list, 
        key=lambda x: x.get('regularMarketChangePercent', 0), 
        reverse=True
    )

    # Prepare it for JSON dump and call it in search views.py
    result = []
    for stock in sorted_gainers:
        symbol = stock.get('symbol')
        percentage = stock.get('regularMarketChangePercent')
        price = Ticker(symbol)

        hist = price.history(period='1d', interval='15m').reset_index()
        price = hist["close"].tolist()
        result.append({
            'ticker':  symbol,
            'price': price,
            'percent': round(float(percentage), 2)

        })
    return result

def dailyLosers():


    s = Screener()
    stocks = s.get_screeners(['day_losers'], count=5)
    gainers_list = stocks.get('day_losers', {}).get('quotes', [])
    sorted_gainers = sorted(
        gainers_list, 
        key=lambda x: x.get('regularMarketChangePercent', 0), 
        reverse=False
    )

    # Prepare it for JSON dump and call it in search views.py
    result = []
    for stock in sorted_gainers:
        symbol = stock.get('symbol')
        percentage = stock.get('regularMarketChangePercent')
        price = Ticker(symbol)

        hist = price.history(period='1d', interval='15m').reset_index()
        price = hist["close"].tolist()
        result.append({
            'ticker':  symbol,
            'price': price,
            'percent': round(float(percentage), 2)

        })
    return result




# Output [{'language': 'en-US', 'region': 'US', 'quoteType': 'EQUITY', 'typeDisp': 'Equity', 'quoteSourceName': 'Delayed Quote', 'triggerable': False, 'customPriceAlertConfidence': 'LOW', 'lastCloseTevEbitLtm': -2692.96816, 'lastClosePriceToNNWCPerShare': 2614.730468229444, 'currency': 'USD', 'bid': 12.78, 'postMarketChange': -0.040000916, 'regularMarketChange': 6.5, 'regularMarketTime': 1767646800, 'regularMarketPrice': 27.04, 'regularMarketDayHigh': 29.43, 'regularMarketDayRange': '23.26 - 29.43', 'regularMarketDayLow': 23.26, 'regularMarketVolume': 1849988, 'regularMarketPreviousClose': 20.54, 'bidSize': 2, 'askSize': 2, 'market': 'us_market', 'messageBoardId': 'finmb_695870118', 'fullExchangeName': 'NasdaqCM', 'longName': 'Regencell Bioscience Holdings Limited', 'regularMarketOpen': 24.0, 'averageDailyVolume3Month': 222263, 'averageDailyVolume10Day': 402740, 'corporateActions': [], 'fiftyTwoWeekLowChange': 26.947212, 'fiftyTwoWeekLowChangePercent': 290.41385, 'fiftyTwoWeekRange': '0.092789 - 83.6', 'fiftyTwoWeekHighChange': -56.559998, 'fiftyTwoWeekHighChangePercent': -0.676555, 'fiftyTwoWeekChangePercent': 16426.0, 'earningsTimestampStart': 1763499600, 'earningsTimestampEnd': 1763499600, 'isEarningsDateEstimate': True, 'trailingAnnualDividendRate': 0.0, 'trailingAnnualDividendYield': 0.0, 'marketState': 'POSTPOST', 'epsTrailingTwelveMonths': -0.01, 'sharesOutstanding': 494488908, 'bookValue': 0.01, 'fiftyDayAverage': 15.9566, 'fiftyDayAverageChange': 11.083401, 'fiftyDayAverageChangePercent': 0.69459665, 'twoHundredDayAverage': 13.722529, 'twoHundredDayAverageChange': 13.3174715, 'twoHundredDayAverageChangePercent': 0.9704823, 'priceToBook': 2704.0002, 'sourceInterval': 15, 'exchangeDataDelayedBy': 0, 'exchangeTimezoneName': 'America/New_York', 'exchangeTimezoneShortName': 'EST', 'gmtOffSetMilliseconds': -18000000, 'ipoExpectedDate': '2021-07-16', 'esgPopulated': False, 'tradeable': False, 'cryptoTradeable': False, 'exchange': 'NCM', 'fiftyTwoWeekHigh': 83.6, 'fiftyTwoWeekLow': 0.092789, 'financialCurrency': 'USD', 'shortName': 'Regencell Bioscience Holdings L', 'ask': 21.88, 'marketCap': 13370980352, 'regularMarketChangePercent': 31.6456, 'hasPrePostMarketData': True, 'firstTradeDateMilliseconds': 1626442200000, 'priceHint': 2, 'postMarketChangePercent': -0.14793238, 'postMarketTime': 1767661190, 'postMarketPrice': 27.0, 'symbol': 'RGC'}]
 

# Reminder: from .models import Profile, Portfolio, StockOrder, StockPosition

# Connect this via url.py in order to connect it in our forms in stock.html

@transaction.atomic
def stockOrder(request, ticker, order_type):
    # Grab the current price of the stock
    stock = Ticker(ticker)
    current_price = Decimal(str(stock.history(period='1d')['close'].iloc[-1]))
    quantity = round(Decimal(request.POST.get('input-changer')), 2)

    # Grab the Portfolio and its owner
    user, _ = Profile.objects.get_or_create(
        username=request.user.username,
        defaults={"email": request.user.email}
    )
    portfolio, _ = Portfolio.objects.get_or_create(
        owner=user,
        defaults={"name": "Main Portfolio"}
    )

    # Grab the stock position of the Ticker and how much quantity does the user have, etc.
    position = StockPosition.objects.filter(user_portfolio=portfolio, ticker=ticker).first()

    # Average Book Cost Formula:  Total Dollar Invested / Quantity Bought

    # Transaction cost 
    capital_user = user.money_owned

    order = StockOrder.objects.create(
        user_portfolio=portfolio,
        ticker=ticker,
        quantity=quantity,
        order_choice=order_type.upper(),
        price_bought=current_price,
        status=StockOrder.Status.PENDING,
    )

    # Grab the Cost for the stock
    transaction = current_price * quantity
    if request.method == "POST":
        if order_type.upper() == StockOrder.OrderChoice.BUY:
            if user.money_owned < transaction:
                order.status = StockOrder.Status.REJECTED
                order.save()
                return redirect("stock", stock_tick=ticker)

            #  We wanna subtract the user's capital with the transaction cost
            # Grab StockPosition book cost
            if not position:
                position = StockPosition.objects.create(
                    user_portfolio=portfolio,
                    ticker=ticker,
                    quantity=quantity,
                    book_cost=current_price,
                )
            else:
                total_cost = (position.book_cost * position.quantity) + transaction
                total_quantity = position.quantity + quantity
                position.quantity = total_quantity
                position.book_cost = total_cost / total_quantity
                position.save()

            user.money_owned -= int(transaction)
            user.save()
            order.status = StockOrder.Status.FILLED
            order.save()

        elif order_type.upper() == StockOrder.OrderChoice.SELL:
            # We'll need to check if the user has the quantity to sell the stock, or
            # even owns the stock XD
            if not position or position.quantity < quantity:
                order.status = StockOrder.Status.REJECTED
                order.save()
                return redirect("stock", stock_tick=ticker)
            # First order of business is to add the money towards its user
            # Since we're selling, AND also subtract stock.quantity 
            user.money_owned += int(transaction)
            position.quantity -= quantity

            # Now if the user sells their stocks (All of it, delete it!)
            # We're also saving data into our models.py
            if position.quantity == 0:
                position.delete()
            else:
                position.save()

            user.save()
            order.status = StockOrder.Status.FILLED
            order.save()

        else:
            order.status = StockOrder.Status.CANCELED
            order.save()
            return redirect("stock", stock_tick=ticker)
        return redirect('stock', stock_tick=ticker)


            


# We will use the federal rates for this endeavour

async def build_stock_analyzer(stock_url, info) -> dict:
    cache_key = f"analysis:{stock_url}"
    
    
    cached = cache.get(cache_key)
    if cached:
        return cached

    
    stock_info = await asyncio.gather(
        sync_to_async(FinancialReport)(stock_url, info),
        sync_to_async(Company_Analysis)(stock_url, info),
        sync_to_async(Revenue_Analysis)(stock_url, info),
        sync_to_async(Growth_Analysis_Outlook)(stock_url, info),
        sync_to_async(Growth_of_Stock)(stock_url, info),
        sync_to_async(Returns_Efficiency_Ratios)(stock_url, info),
        sync_to_async(Company_Debt)(stock_url, info),
        sync_to_async(bullish)(stock_url),
    )
    

    results = {
        "Financial Reports": html_to_paragraph_text(markdown.markdown(stock_info[0])),
        "Company Analysis": html_to_paragraph_text(markdown.markdown(stock_info[1])),
        "Profitability Metrics": html_to_paragraph_text(markdown.markdown(stock_info[2])),
        "Profit Analysis Outlook": html_to_paragraph_text(markdown.markdown(stock_info[3])),
        "Growth of Stock": html_to_paragraph_text(markdown.markdown(stock_info[4])),
        "Returns Efficiency": html_to_paragraph_text(markdown.markdown(stock_info[5])),
        "Company Debt": html_to_paragraph_text(markdown.markdown(stock_info[6])),
        "Bullish Summary": html_to_paragraph_text(markdown.markdown(stock_info[7])),
    }
    cache.set(cache_key, results, timeout=60 * 30)
    return results
async def build_etf_analyzer(stock_url) -> dict:
    cache_key = f"analysis:{stock_url}"
        
    
    cached = cache.get(cache_key)
    if cached:
        return cached

    
    stock_info = await asyncio.gather(
        sync_to_async(ETF_FinancialReport)(stock_url),
        sync_to_async(bullish)(stock_url),
    )

    results = {
        "Financial Reports": html_to_paragraph_text(markdown.markdown(stock_info[0])),
        "Bullish Summary": html_to_paragraph_text(markdown.markdown(stock_info[1])),
    }
    cache.set(cache_key, results, timeout=60 * 30)
    return results

# I forgot to connect it in my url router 💀

def json_data_api(date_api:str, stock: str) -> dict:
    # Grab stock information for our graphs and also exchangeNames and CompanyNames for
    # our UI
    """ This will prepare our data from YahooQuery in to create a graph, Long Names, and Exchanges for better UI/UX. 
    Arguments(): Data API will be used for us to connect with the buttons to change the graph of the stock via intervals. We'll be using date_api statements to create an interval.
    Stock is mostly reliant from our stock views. We can neglect stock checker
    

    """
    
    stock = stock.upper()
    ticker = Ticker(symbols=stock)
    summary = ticker.price.get(stock, {})
    company_name = summary.get("shortName") or summary.get("longName")
    exchange =  summary.get("exchangeName")
    date = summary.get("regularMarketTime")

    # Important resources: https://ranaroussi.github.io/yfinance/
    
    market_state = summary.get('marketState')

    # We want to make the value of afterhours none for now.
    # We'll also need this for my bullish indicator because I have one data that could change the bullish indicator itself

    # Formula needed: After Hours Return  = ((RostMarket - RegClose) / regClose)* 100
    after_hours = None
    



    if date_api == '1D':
        period = '1d'
        interval = '1m'
        yester_interval = '1d'
        period_inter = '2d'
        interval_format = '%a %H:00'
        
    elif date_api == '1W':
        period = '1wk'
        interval = '15m'
        yester_interval = '1wk'
        period_inter = '2wk'
        interval_format = '%a %H:%M'
    elif date_api == '1M':
        period = '1mo'
        interval = '1h'
        yester_interval = '1mo'
        period_inter = '2mo'
        interval_format = '%b %d'
        
    # Do years
    elif  date_api == '1Y':
       period = '1y'
       interval = '1wk'

       period_inter = '2y'     
       yester_interval = '1mo'   
       interval_format = '%Y-%b'

    stock_bars = ticker.history(period=period, interval=interval)
    
    stock_bars = stock_bars.reset_index()

    stock_bars['date'] = pd.to_datetime(stock_bars['date'])


    yesterday_price = ticker.history(period=period_inter, interval=yester_interval)
    yesterday_price_data = yesterday_price.iloc[-2]["close"]
 

    graph_label = stock_bars['date'].dt.strftime(interval_format).tolist()
    graph_price = stock_bars['close'].tolist()


    return {
        'chart_label': graph_label,
        'chart_price': graph_price,
        'name': company_name,
        'exchange': exchange,
        'date': date,
        'yesterday_price': yesterday_price_data,
    }

def json_data_view(request, stock, interval):
    api_data = json_data_api(interval.upper(), stock)
    response_data = {
        "labels": api_data["chart_label"],
        "prices": api_data["chart_price"],
        "yesterday_price": api_data["yesterday_price"]
    }
    return JsonResponse(response_data, safe=True)

# Output: {'maxAge': 1, 'preMarketSource': 'FREE_REALTIME', 'postMarketChangePercent': -0.00018197265, 'postMarketChange': -0.049316406, 'postMarketTime': '2026-01-02 17:59:55', 'postMarketPrice': 270.9607, 'postMarketSource': 'FREE_REALTIME', 'regularMarketChangePercent': -0.00312652, 'regularMarketChange': -0.849976, 'regularMarketTime': '2026-01-02 14:00:00', 'priceHint': 2, 'regularMarketPrice': 271.01, 'regularMarketDayHigh': 277.8248, 'regularMarketDayLow': 269.02, 'regularMarketVolume': 37746172, 'regularMarketPreviousClose': 271.86, 'regularMarketSource': 'FREE_REALTIME', 'regularMarketOpen': 272.05, 'exchange': 'NMS', 'exchangeName': 'NasdaqGS', 'exchangeDataDelayedBy': 0, 'marketState': 'CLOSED', 'quoteType': 'EQUITY', 'symbol': 'AAPL', 'underlyingSymbol': None, 'shortName': 'Apple Inc.', 'longName': 'Apple Inc.', 'currency': 'USD', 'quoteSourceName': 'Nasdaq Real Time Price', 'currencySymbol': '$', 'fromCurrency': None, 'toCurrency': None, 'lastMarket': None, 'marketCap': 4021894250496}

# Grab the Autocomplete Stock

# async def get_stock_suggestion(request):
#     query = request.GET.get('term', '')


# Grab name and ztock price used for our html. The difference is that we can do async call from Javascript in order to update it constantly

@sync_to_async
def grab_current_price(stock: str) -> dict:
    stock = stock.upper()
    result_search = Ticker(stock)
    price = result_search.history(period="1d")["close"].iloc[-1]

    if price > 10:
        return float(round(price, 1))
    elif price > 4.5:
        return float(round(price, 2))
    else:
        return float(round(price, 3))
    
async def latest_price(request, stock):
    price = await grab_current_price(stock=stock)
    return JsonResponse({"price": price})



# This will be for our autocomplete stuff


API_KEY = os.getenv('ALPACA')


ALPACA_SECRET_KEY  = os.getenv('ALPACA_SECRET_KEY')





alpaca_client = TradingClient(api_key=API_KEY, secret_key=ALPACA_SECRET_KEY , paper=True)



@sync_to_async
def autocomplete(data: str):
    # Do multi-key sort

    # Ensure add caching in order to make the performance better of this autocomplete program
    # It's valid as the stock market wouldn't change by a lot and the existing stocks would ensure that caching 
    # will be the best choice for the memory management.

    cache_key = f"autocomplete:{data}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    ASSET_CACHE_KEY = "alpaca_all_assets"

    cache_asset = cache.get(ASSET_CACHE_KEY)

    TOP_EXCHANGE = {
        'NASDAQ': 0,
        'NYSE': 0,
        

    }
    
    data = data.upper()

    stock_param = GetAssetsRequest(
        status= AssetStatus.ACTIVE,
        asset_class= AssetClass.US_EQUITY,

    )
    asset = alpaca_client.get_all_assets(stock_param)
    cache.set(ASSET_CACHE_KEY, asset, 86400)
    
    FORBIDDEN_EXCHANGE = ['ARCA', 'OTC']
    
    # Stock rec using  list comp
        
    # We want to short via marketCapshare for the trendiest stock to be int he top of the autocomplete.
    # For better User Experience
    # Filter out Leverage ETF, and OTC.


    RESTRICTED_WORD = 'ETF'
    stock_rec = [a for a in asset if a.symbol.upper().startswith(data.upper()) and a.tradable and (a.exchange.value not in FORBIDDEN_EXCHANGE) 
                    and (a.exchange.value != 'BATS') and RESTRICTED_WORD not in (a.name or '').upper() ][:80]
    
    
    
    stock_ticker = Ticker(symbols=stock_rec)

    data_price = stock_ticker.price
    # Needed for popularity of stock sorting

    def grab_market_cap(esc):
        return data_price.get(esc, {}).get("marketCap", 0) or 0
    def grab_top_exchange_rate(a):
        return TOP_EXCHANGE.get(a.exchange, 1)
    def grab_volume(sym):
        return data_price.get(sym, {}).get('regularMarketVolume',  0) or 0
    
    
    stock_rec.sort(
        key=lambda a: (
            grab_market_cap(a.symbol),
            grab_volume(a.symbol),
            grab_top_exchange_rate(a),

        ),
        reverse=True
    )

    result = stock_rec[:11]
    cache.set(cache_key, result, timeout=60 * 5)
    
    return result


    
    
        # We want to short via marketCapshare for the trendiest stock to be int he top of the autocomplete.



# Output: [{'exchange': 'NYQ', 'shortname': 'Agilent Technologies, Inc.', 'quoteType': 'EQUITY', 'symbol': 'A', 'index': 'quotes', 'score': 10046500.0, 'typeDisp': 'Equity', 'longname': 'Agilent Technologies, Inc.', 'exchDisp': 'NYSE', 'sector': 'Healthcare', 'sectorDisp': 'Healthcare', 'industry': 'Diagnostics & Research', 'industryDisp': 'Diagnostics & Research', 'dispSecIndFlag': False, 'isYahooFinance': True}, {'exchange': 'NYM', 'shortname': 'Platinum Apr 26', 'quoteType': 'FUTURE', 'symbol': 'PL=F', 'index': 'quotes', 'score': 3003200.0, 'typeDisp': 'Futures', 'exchDisp': 'NY Mercantile', 'isYahooFinance': True}, {'exchange': 'CMX', 'shortname': 'Aluminum Futures,Mar-2026', 'quoteType': 'FUTURE', 'symbol': 'ALI=F', 'index': 'quotes', 'score': 3000600.0, 'typeDisp': 'Futures', 'exchDisp': 'New York Commodity Exchange', 'isYahooFinance': True}, {'exchange': 'NGM', 'quoteType': 'EQUITY', 'symbol': 'SVAQU', 'index': 'quotes', 'score': 100004.0, 'typeDisp': 'Equity', 'longname': 'Silicon Valley Acquisition Corp.', 'exchDisp': 'NASDAQ', 'sector': 'Financial Services', 'sectorDisp': 'Financial Services', 'industry': 'Shell Companies', 'industryDisp': 'Shell Companies', 'isYahooFinance': True}, {'exchange': 'NCM', 'quoteType': 'EQUITY', 'symbol': 'NBRGU', 'index': 'quotes', 'score': 100002.0, 'typeDisp': 'Equity', 'longname': 'Newbridge Acquisition Limited', 'exchDisp': 'NASDAQ', 'sector': 'Financial Services', 'sectorDisp': 'Financial Services', 'industry': 'Shell Companies', 'industryDisp': 'Shell Companies', 'isYahooFinance': True}, {'exchange': 'NGM', 'quoteType': 'EQUITY', 'symbol': 'IGACR', 'index': 'quotes', 'score': 100001.0, 'typeDisp': 'Equity', 'longname': 'Invest Green Acquisition Corporation', 'exchDisp': 'NASDAQ', 'isYahooFinance': True}, {'exchange': 'CCY', 'shortname': 'AUD/USD', 'quoteType': 'CURRENCY', 'symbol': 'AUDUSD=X', 'index': 'quotes', 'score': 30109.0, 'typeDisp': 'Currency', 'longname': 'AUD/USD', 'exchDisp': 'CCY', 'isYahooFinance': True}]


# Bullish Indicator


    

    






async def information_letter(request, letters):
    quotes = await autocomplete(letters)
    results = []
    for q in quotes:
        results.append({
        'symbol': q.symbol ,
        'name': q.name or '',
        'exchange': q.exchange,
    })


    return JsonResponse({'results': results})




def check_stock(stock):
    try:
        ticker = yf.Ticker(stock)
        # We can do is if something doesn't return, we can do return None 
        # and in Search
        info = ticker.info
        
        day_stock_data = ticker.history(period='1d')

        stock_info = {
            'ticker': stock,
            'price': day_stock_data,
        }
    
    

        if not info or 'regularMarketPrice' not in info:
                return messages.error("The stock does not exist. Please try again")

            
        return stock_info

    # except (ValueError, ConnectionAbortedError, ConnectionError, KeyError, IndexError):
    #     return None
    except Exception as e:
    # Catch JSONDecodeError and any unexpected error
        print(f"Error fetching stock {stock}: {e}")
        return None






def search(request):
    print("AUTH USER:", request.user, request.user.is_authenticated)

    # This is the index view where we will display the home page/search page
    # Now we need to find how to redirect the search html -> stock.html
    if request.method == "GET":
        # AAPL, etc
        search_stock = request.GET.get("search")
                
        if search_stock:
            search_stock = str(search_stock.upper())

        # ask for check_stocks
            stock_checked = check_stock(stock=search_stock)

            if stock_checked is None:
                messages.error(request, "Please Try Again, This Stock Does not Exist")
                return redirect('search')

    
            # This will give the stock the i = stock_checked. Since it's existing right?
            else:
                return redirect('stock', stock_tick=search_stock)
    # Mistake: We forgot it was a list. So we hav eto use list comphrension to get the data needed
    data_json =  dailyWinners()
    data_json_loser = dailyLosers()

    label_loser_ticker = json.dumps([item['ticker'] for item in data_json_loser])
    label_loser_percentage = json.dumps([item['price'] for item in data_json_loser])

    label_ticker = json.dumps([item['ticker'] for item in data_json])
    label_percentage = json.dumps([item['price'] for item in data_json])
    gainers = {
        'gainers': data_json,
        'loser': data_json_loser,
        'label_ticker': label_ticker,
        'label_percentage': label_percentage,
        'label_loser_ticker': label_loser_ticker,
        'label_loser_percentage': label_loser_percentage

    }
    


            
    # Grab the json_dump
        # Now check if the stock exists
    return render(request, 'base/search.html', gainers)





def stock(request, stock_tick:str):

    # This will happen when the user has: Search.html -> Stock Checker ->

    
    

    stock_url = stock_tick.upper()

    info = StockInfo(stock_url)

    date_time = request.GET.get('interval', '1D')
    
    
    for i in ticker:
        
        if i['id'] == str(stock_tick):
            
            stock_url = i

    stock_url = stock_tick.upper()  
    # placeholder, we don't want to call position unless the user is authenticated, and also owns the stock. Dataset we want: Position, Shares owned, average cost.
    position = None
    shares_owned = 0
    avg_cost = None
    # We need to add if user is authetnicated   
    # Grab Position, 
   
    if request.user.is_authenticated:
        position = StockPosition.objects.filter(
        user_portfolio__owner__username=request.user.username,
        ticker=stock_url
        
        ).first()
        user, _ = Profile.objects.get_or_create(
        username=request.user.username,
        defaults={"email": request.user.email}
        )

        
        user_capital = user.money_owned

        if position:
            shares_owned = position.quantity
            avg_cost = position.book_cost
    



    

    # Gather Json data API
    # Not needed for Async.
    data_json =  json_data_api(date_api=date_time, stock=stock_url)


    label_graph = json.dumps(data_json['chart_label'])
    label_price = json.dumps(data_json['chart_price'])

    exchange = data_json["exchange"]
    stock_name = data_json["name"]
    date = data_json["date"]

    if is_etf(stock=stock_url):
        data_stock = async_to_sync(build_etf_analyzer)(stock_url=stock_url)


    # needed

    else:
        data_stock = async_to_sync(build_stock_analyzer)(stock_url=stock_url, info=info)



    # Grab the yesterday price so that we can change the colour of the graph depending if it's green or red.
    yesterday_price = data_json["yesterday_price"] or 0
    
    # NEEDED for bullish chart.js
    points = bullish_indicator(stock=stock_url)

    capm_score_of_stock = capital_asset_pricing_models(ticker=stock_url)

    context = {'ticker': ticker, 'information_of_stock': data_stock, 'stock_graph': label_graph, 'stock_price':
               label_price, "exchange": exchange, "longName": stock_name, "date": date, "bullish_indicator": points, "yesterday_price": yesterday_price,     "shares_owned": shares_owned,
               "avg_cost": avg_cost, 'capital': user_capital, 'capm_score_of_stock': capm_score_of_stock, }

    return render(request, 'base/stock.html', context)


def portfolio(request):
    return render(request, 'base/portfolio_room.html')

def signup(request):

    # We need to gather information, and we also need to check if the username exists in the database. If it does not, it shall proceed towards the signup, if not then we'll add a message_flash to warn user that the username exists in the database.
    if request.method == 'POST':
        email = request.POST.get('email')

        
        username = request.POST.get('username')
        
        password = request.POST.get('password')

        
        if User.objects.filter(username=username).exists():
            messages.error(request, "This username already exists, please try again!")
            return render(request, 'base/authentication/signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "This email already exists in the database, please try again!")
            return render(request, 'base/authentication/signup.html')
        else:
        
            user = User.objects.create_user(username=username, password=password, email=email)
        
            messages.success(request, "Successfully Signed up, please use login page!")
       
            redirect("base/authentication/login.html")

    return render(request, 'base/authentication/signup.html')





def loginpage(request):
    
    recent_url = request.GET.get('next') or request.POST.get('next') or 'search'

    if request.user.is_authenticated:
       return redirect('search')
      
    # Check if user exists in the database, if not we can do a 

    if request.method == "POST":
        email =  request.POST.get('email')

        password = request.POST.get('password')

        # This will check if user authentication will exist
        user = authenticate(request, email=email , password=password)

        if user is None:
            messages.error(request, "This user does not exist, please signup or try again!")
            return render(request, 'base/authentication/login.html')


      
        login(request, user)
        messages.info(request, "Login successful! Enjoy MarketSight!")
        return redirect(recent_url)
        
    return render(request, 'base/authentication/login.html')

def logout_page(request):
    
    logout(request)
    
    return redirect('search')



def assistance(request):

    # We want user to be in the database: Email, and  Username

    # If it doesn't exist, we want it to have an error 

    if request.method == "POST":
        name = request.POST.get('name')
        
        email = request.POST.get('email')

        user_message  = request.POST.get('message')

        subject = request.POST.get('subject')
        
        user = authenticate(request, email=email, username=name)

        send_mail (
            subject = f"New Contact Message from {subject}",
            message= f"from {name} \n {user_message }",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER], 


        )
        messages.success(request, "Login successful! Enjoy MarketSight!")
        return render(request, 'base/search.html')


    return render(request, 'base/Assistance.html')






# I

#  Create the login html, I will be using password redirects later



def portfolio_room(request, date='1D'):
    # We will fetch user's stock portfolio from database and display it here, so our context would have ticker, and create average return. 

    # Important Formula: \(\text{ROI}=\left(\frac{\text{Final\ Value\ of\ Investment}-\text{Total\ Cost\ of\ Investment}}{\text{Total\ Cost\ of\ Investment}}\right)\times 100\%\)

    #  Create a sidebar with graphs, ticker name, etc,.and we grab those information from StockPosition

    # First grab stockPositon

    # check if user is authenticated:
    if not request.user.is_authenticated:
        redirect ('search')


    user_stock_position = StockPosition.objects.filter(
    user_portfolio__owner__username=request.user.username
)
    # Iterate through it :)
    result_of_stock = []
    list_of_user_stock = user_stock_position.values_list('ticker', flat=True)
    # Side bar, we'd need the price of the stock (For the graph and url router) 
    # Also grab the percentage of the stock. Use ROI average aggeragation.
    # Add the portoflio's position value of the stock / initial_investment.


    # So current value / cost


    

    
    if date == '1D':
        period = '1d'
        interval = '1m'
        interval_format = '%a %H:00'
        
    elif date == '1W':
        period = '1wk'
        interval = '15m'
        interval_format = '%a %H:%M'
    elif date == '1M':
        period = '1mo'
        interval = '1h'
        interval_format = '%b %d'
        
    # Do years
    elif  date == '1Y':
       period = '1y'
       interval = '1wk'
  
       interval_format = '%Y-%b'

    ticker_list = list(user_stock_position.values_list('ticker', flat=True))

    ticker_api_query = Ticker(ticker_list, asynchronous= True)
    ticker_htst =  ticker_api_query.history(period=period, interval=interval)
   

    # I want to grab the value of the stock that portfolio user has.....

    # We also want to grab the user's total value, so therefore keep a value that keeps track with all of them

    sum_of_user_portfolio = 0
    cost_of_user_portfolio = 0
    for position in (user_stock_position):
        ticker = position.ticker

        quantity = float(position.quantity)
        avg_cost = float(position.book_cost)

        

     
        
        result_search = Ticker(ticker)
        current_price = result_search.history(period=period)["close"].iloc[-1]
        # sum += price * quantity
        
        sum_of_user_portfolio += current_price * quantity
        cost_of_user_portfolio += avg_cost * quantity



        # Another thing we can do is find avg_cost * quantity and do total rate of return of the user's investment




        price = ticker_htst.loc[ticker]['close'].tolist()
        # We can switch this if we ever want to, I have a future plan :)
        time_labels = [t.strftime(interval_format) for t in ticker_htst.loc[ticker].index]


        # We need
        result_of_stock.append({
            'ticker': ticker,
            'price': price,
            'quantity': quantity,
            'book_cost': avg_cost,
            'date': time_labels,
            'current_price': current_price,

        })


    


    # We want to also grab the total value of the stock, iterate through user position, and we'd want to compare this in javascript, so I can create better UI for the graph.
    # Grab quantity:   # Grab the ticker price

    # Value of the stock; grab_price * user.quamtity


    # Now this is where we grab our information from our chart

    # Grab the ticker list and we can do is make another dict and use list comp to manipulate the data in order to get the arrays for data set.

    # Grab user profile
    profile, _ = Profile.objects.get_or_create(username=request.user.username,
                                                 defaults={'email': request.user.email})
    context = {
        'stock': result_of_stock,
        'cost_of_user_portfolio': cost_of_user_portfolio,
        'capital': round(profile.money_owned, 2),
        'json_data_set_stocks': json.dumps(result_of_stock),
        'portfolio_val': round(sum_of_user_portfolio, 2),
    }

    return render(request, 'base/portfolio_room.html', context)




