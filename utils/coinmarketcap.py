from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from pathlib import Path
import pandas as pd
import json
import os

from dotenv import load_dotenv
load_dotenv()

## Our coinbase Data Retrieval Library
cmc_sandbox_listings_url = os.getenv("X-CMC_SANDBOX_LISTINGS_URL")
cmc_id = os.getenv("X-CMC_PRO_API_KEY")

cmc_sandbox_url = "https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"


def test(url):
    
    parameters = {
      'start':'1',
      'limit':'5000',
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': cmc_id,
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      # data = json.loads(response.text)
      data = response.text
      print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

    return
