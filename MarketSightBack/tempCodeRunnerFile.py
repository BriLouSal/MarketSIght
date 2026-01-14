from alpaca.trading.client import TradingClient
from alpaca.data.historical  import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca_trade_api import REST
from alpaca.common.exceptions import APIError # This is to ensure to check stocks (which will lead to API Error when a Stock is not valid)

from datetime import datetime, timedelta, timezone


import re

import json
from json import JSONDecodeError


from anthropic import AnthropicVertex
from anthropic import Anthropic



# from .training_models import positivity_rating

import os
from dotenv import load_dotenv


from yahooquery import Ticker

import pandas as pd

import json

load_dotenv()



API_KEY = os.getenv('ALPACA')


SECRET_KEY = os.getenv('SECRET_KEY')


CLAUDE = os.getenv('CLAUDE')


alpaca_client = TradingClient(api_key=API_KEY, secret_key=SECRET_KEY)






client = Anthropic(api_key=CLAUDE)

MODEL_AI = "claude-sonnet-4-5"

MAX_TOKENS = os.getenv('MAX_TOKENS')
MAX_TOKEN_FOR_NEWS_SENTIMENT = os.getenv('MAX_TOKEN_FOR_NEWS_SENTIMENT')
MAX_TOKENS_ANALYSIS_ON_NEWS = os.getenv('MAX_TOKENS_ANALYSIS_ON_NEWS')

tools = {}


def gen_ai_parser(text: str):
    sentences = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        line = re.sub(r"^\d+\s*[\.\)]\s*", "", line)
        sentences.append(line)
    return sentences


def check_stock(stock: str) -> str:
    try:
        asset = alpaca_client.get_asset(stock.upper())
        if asset:
            return True
        else:
            return False
    

    except APIError as e:
        # We can have an if-statement on
        return False
# I want to create a summary of the stock 

# MUST BE A STRING
def StockInfo(symbol: str) -> str:
    # First check stock
    symbol = symbol.upper()
    stock = Ticker([symbol])
    financial_data = stock.financial_data.get
    financial_data = stock.financial_data.get(symbol, {})
    return financial_data


def FinancialReport(stock: str) -> str:
    stock = stock.upper()
    dict_information = StockInfo(stock)
    financial_information = {
        "currentPrice": dict_information.get("currentPrice"),
        "targetLowPrice": dict_information.get("targetLowPrice"),
        "targetMeanPrice": dict_information.get("targetMeanPrice"),
        "targetMedianPrice": dict_information.get("targetMedianPrice"),
        "targetHighPrice": dict_information.get("targetHighPrice"),
        "recommendationMean": dict_information.get("recommendationMean"),
        "recommendationKey": dict_information.get("recommendationKey"),
        "recommendationKey": dict_information.get("recommendationKey"),

    }
    stock = stock.upper()
    information_of_stock = StockInfo(stock)
    # Check if stock exist,  if it deos pass response and return it
    if check_stock(stock):
        financial_info = client.messages.create(
            model=MODEL_AI,
            max_tokens=int(MAX_TOKENS),
            messages=[
                {"role": "user", 
                "content": f"Summarize  stock information {financial_information} and the updates it should have such as that it has it properly formmated such as that we're able to have it organized prompt, and we want it to be formmated and useable in Django (NO CODE, BUT THIS IS  A REFERENCE TO JUST FORMAT IT HAHA. DO NOT ADD THE REMAINING FORMALITY, JUST ADD INFORMATION ONLY!). What does the stock infomration entail the company and what should investors do when investing in {stock}. Format it in a way that is good for Django (Do not write code, just format the words and summary really well that it's compatible in HTML). Using the information in {financial_information} Please generate it such as that it's organized that would fit as a paragraph in django, and I want it to be really great formatted. So whatever you had in the {financial_information} Will be formatted perfectly with the best of your ability, just add it and no formalities... Make sure it's detailed and dumb down for retail investors such as I in what information entails per each subject and how does it impact future growth and stock. Make sure the information is DUMBED enough for retail investors, why is it important, etc. Ensure that infomration is detailed for each subject such as Profitability Metrics, etc.  Please have it detailed around A LOT OF WORDS AND  HAVE IT LIKE YOU'RE A HIGH FIRM CONSULTANT INVESTORS FUND AND I WANT YOU TO DUMB IT DOWN FOR RETAIL INVESTORS, AND I WANT IT FORMATTED LIKE THIS:\n"
                "- Output ONLY JSON.\n"
                "- JSON must be valid.\n"
                "- No backticks.\n"
                "- No extra text.\n"
                "- No disclaimers.\n"}
            ],
        )

            # Create a max tokens for users, MAKE SURE TO ADD THE MAX TOKEN VALUE IN ENV
        return financial_info.content[0].text.strip()

    else:
        return f"The Stock {stock} Does not Exist, Please Try Again!"   

def StockSummary(stock: str) -> str:
    stock = stock.upper()
    information_of_stock = StockInfo(stock)
    # Check if stock exist,  if it deos pass response and return it
    if check_stock(stock):
        financial_info = client.messages.create(
            model=MODEL_AI,
            max_tokens=int(MAX_TOKENS),
            messages=[
                {"role": "user", 
                "content": f"Summarize  stock information {information_of_stock} and the updates it should have such as that it has it properly formmated such as that we're able to have it organized prompt, and we want it to be formmated and useable in Django (NO CODE, BUT THIS IS  A REFERENCE TO JUST FORMAT IT HAHA. DO NOT ADD THE REMAINING FORMALITY, JUST ADD INFORMATION ONLY!). What does the stock infomration entail the company and what should investors do when investing in {stock}. Format it in a way that is good for Django (Do not write code, just format the words and summary really well that it's compatible in HTML). Using the information in {information_of_stock} Please generate it such as that it's organized that would fit as a paragraph in django, and I want it to be really great formatted. So whatever you had in the {information_of_stock} Will be formatted perfectly with the best of your ability, just add it and no formalities... Make sure it's detailed and dumb down for retail investors such as I in what information entails per each subject and how does it impact future growth and stock. Make sure the information is DUMBED enough for retail investors, why is it important, etc. Ensure that infomration is detailed for each subject such as Profitability Metrics, etc.  Please have it detailed around A LOT OF WORDS AND  HAVE IT LIKE YOU'RE A HIGH FIRM CONSULTANT INVESTORS FUND AND I WANT YOU TO DUMB IT DOWN FOR RETAIL INVESTORS, AND I WANT IT FORMATTED LIKE THIS:"}
            ],
        )

            # Create a max tokens for users, MAKE SURE TO ADD THE MAX TOKEN VALUE IN ENV
        return financial_info.content[0].text.strip()

    else:
        return f"The Stock {stock} Does not Exist, Please Try Again!"   

def news(stock: str) -> str:
    
    stock = stock.upper()
    api_rest = REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')
    end = datetime.now(timezone.utc).date()
    start = (end - timedelta(days=7))

    news_article = api_rest.get_news(symbol=stock, start=start.isoformat(), end=end.isoformat(), include_content=True)



    # Empty dict that will be appended

    result = {}

    for article in news_article:
        headline = (getattr(article, "headline", "") or "").strip()
        content  = (getattr(article, "content", "") or "").strip()
        if not content:
            content = (getattr(article, "summary", "") or "").strip()
        if headline:
            return {"Headline": headline, "Content": content}


    return None

    


# Summary returns markdown
def NewsSummary(stock: str) -> str:
    stock = stock.upper()
    # Check if stock exist,  if it deos pass response and return it
    if check_stock(stock):
        information_of_stock = news(stock)
        news_information = client.messages.create(
            model=MODEL_AI,
            max_tokens=int(MAX_TOKENS),
            messages=[
                {"role": "user", 
                 "content": f"Summarize news informationof {information_of_stock} such as that it's formatted really well and ignore formallities such as that summarized {information_of_stock} is the main mission. Add recently and what is the intended ramification of the stock news.  Will be formatted perfectly with the best of your ability, just add it and no formalities... Make sure it's detailed and dumb down for retail investors such as I in what information entails per each subject and how does it impact future growth and stock. . What does the stock infomration entail the company and what should investors do when investing in {stock}. Format it in a way that is good for Django (Do not write code, just format the words and summary really well that it's compatible in HTML)."}
            ],
        )

            # Create a max tokens for users, MAKE SURE TO ADD THE MAX TOKEN VALUE IN ENV
        return news_information.content[0].text.strip()
    else:
        return f"The Stock {stock} Does not Exist, Please Try Again!"
    
def info_to_positivty_rating_positivety():
    positive_data = client.messages.create(
    model=MODEL_AI,
    max_tokens=int(MAX_TOKEN_FOR_NEWS_SENTIMENT),
    messages =[
        {"role": "user", 
            "content": f"Generate 100 short, realistic, positive financial news headlines about fictional U.S. publicly traded companies. Each headline must represent a catalyst that would reasonably push a stock upward. Keep each headline between 12–22 words. that would be only for sci-kit training. All companies must sound realistic but must not match any real companies. The sentiment should clearly fall within the positive range (0.70–1.00).  Do NOT mention sentiment scores in the output.  Do NOT number the items. Return ONLY the headlines, one per line, no formatting, no markdown."}
    ],
)
    text = (positive_data.content[0].text.strip())

    return gen_ai_parser(text)

def info_to_positivty_rating_netural():
    netural_data = client.messages.create(
    model=MODEL_AI,
    max_tokens=int(MAX_TOKEN_FOR_NEWS_SENTIMENT),
    messages =[
        {"role": "user", 
            "content": f"Generate 100 short, realistic, netural financial news headlines about fictional U.S. publicly traded companies. Each headline must represent a catalyst that would reasonably push a stock upward. Keep each headline between 12–22 words. that would be only for sci-kit training. All companies must sound realistic but must not match any real companies. The sentiment should clearly fall within the netural range (0.45–0.55).  Do NOT mention sentiment scores in the output. Do NOT number the items. Return ONLY the headlines, one per line, no formatting, no markdown."}
    ],
)

    text = (netural_data.content[0].text.strip())

    return gen_ai_parser(text)



def info_to_positivty_rating_negative():

    negative_data = client.messages.create(
    model=MODEL_AI,
    max_tokens=int(MAX_TOKEN_FOR_NEWS_SENTIMENT),
    messages =[
        {"role": "user", 
            "content": f"Generate 100 short, realistic, negative financial news headlines about fictional U.S. publicly traded companies. Each headline must represent a catalyst that would reasonably push a stock upward. Keep each headline between 12–22 words. that would be only for sci-kit training. All companies must sound realistic but must not match any real companies. The sentiment should clearly fall within the negative range (0.00-0.30).  Do NOT mention sentiment scores in the output.  Do NOT number the items. Return ONLY the headlines, one per line, no formatting, no markdown."}
    ],
)
    text = (negative_data.content[0].text.strip())

    return gen_ai_parser(text)






# Create a Portfolio summary via creating,
    
def portfolio_summary(stock: str) -> dict:
    pass





print(FinancialReport(stock='AAPL'))