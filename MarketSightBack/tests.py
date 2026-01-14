from django.test import TestCase

# Create your tests here.


import requests
from bs4 import BeautifulSoup



url = "https://ca.finance.yahoo.com/markets/stocks/gainers/"

url_request = requests.get(url)

print(url_request.text)




