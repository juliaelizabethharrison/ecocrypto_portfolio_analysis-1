import os
import pandas as pd
import requests
import json
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

## Our coinbase Data Retrieval Library
cb_pro = os.getenv("COINBASE_PRO_FQDN")
cb_pub = os.getenv("COINBASE_PUB_FQDN")
cb_sandbox = os.getenv("COINBASE_SANDBOX_FQDN")

def sleep(t):
    time.sleep(t)
    return
    
def fetch_product_trades(product):
    """
    Returns DataFrame for product trades
    
    """
    trades_url = f"{cb_pub}/products/{product}/trades?limit=1000"
    headers = {"Accept": "application/json"}
    trades_columns = ["time","trade_id","price","size","side"]
    response = requests.get(trades_url, headers=headers)

    if response.status_code == 200:
        trades_df = pd.DataFrame(json.loads(response.text), columns=trades_columns)
        trades_df['date'] = pd.to_datetime(trades_df['time'])  # convert to a readable date
        today = datetime.today().strftime('%Y-%m-%d')

        if trades_df is None:
            print("Did not return any data from Coinbase for this symbol")
        else:
            filename = f'data/coinbase_{product}_trades_{today}.csv'
            trades_df.to_csv(filename, index=False)
            print(f'Created CSV file: {filename}.')
    else:
        print("Did not receieve OK response from Coinbase API")
        print(response.text)
        
    # sleep(10)
    return trades_df

def fetch_product_candles(product):
    """
    Returns DataFrame for product candles
    
    """
    url = f'{cb_pub}/products/{product}/candles?granularity=86400' ## &start={candle_start}&end={candle_end}'
    response = requests.get(url)
    if response.status_code == 200:
        candles_df = pd.DataFrame(json.loads(response.text), columns=['unix', 'low', 'high', 'open', 'close', 'volume'])
        candles_df['date'] = pd.to_datetime(candles_df['unix'], unit='s')  # convert to a readable date
        candles_df['vol_fiat'] = candles_df['volume'] * candles_df['close'] # multiply the BTC volume by closing price to approximate fiat volume
        today = datetime.today().strftime('%Y-%m-%d')

        if candles_df is None:
            print("Did not return any data from Coinbase for this symbol")
        else:
            filename = f'data/coinbase_{product}_candles_{today}.csv'
            candles_df.to_csv(filename, index=False)
            print(f'Created CSV file: {filename}.')
    else:
        print("Did not receieve OK response from Coinbase API")

    # sleep(10)
    return candles_df


def fetch_product_ticker(product):
    """
    Returns json text response for product ticker header
    
    """
    ticker_url = f"{cb_pub}/products/{product}/ticker"
    headers = {"Accept": "application/json"}
    response = requests.get(ticker_url, headers=headers)

    if response.status_code == 200:
        return dict(json.loads(response.text))
    else:
        print("Did not receieve OK response")
        return None

# Get a specific product stats
def fetch_product_stats(product):
    """
    Returns json text response for product stats header
    
    """

    stats_url = f"{cb_pub}/products/{product}/stats"
    headers = {"Accept": "application/json"}
    response = requests.get(stats_url, headers=headers)

    if response.status_code == 200:
        return dict(json.loads(response.text))
    else:
        print("Did not receieve OK response")
        return None

def get_currencies():
    """
    Returns DataFrame of currencies available on coinbase exchange.
    
    """
    coin_url = f"{cb_pub}/currencies"
    coin_response = requests.get(coin_url)
    if coin_response.status_code == 200:
        filename = "data/coinbase_currencies.csv"
        currencies_df = pd.DataFrame(json.loads(coin_response.text), columns=['id', 'name', 'min_size', 'status', 'max_precision']).fillna('')
        currencies_df.to_csv(filename, index=False)
        print(f"Created CSV file: {filename}")
    else:
        print(f"Did not receive 200 response")
 
    return currencies_df

def get_products():
    """
    Returns a listing of data products that are available

    """
    product_url = f"{cb_pub}/products"
    headers = {"Accept": "application/json"}
    product_response = requests.get(product_url, headers=headers)
    product_columns=["id","base_currency","quote_currency","base_min_size","base_max_size","quote_increment","base_increment","display_name","min_market_funds","max_market_funds","margin_enabled","fx_stablecoin","max_slippage_percentage","post_only","limit_only","cancel_only","trading_disabled","status","status_message","auction_mode"]
    
    # if product_response.status.code == 200:  NOTE:  This endpoint doesn't send any response code
    filename = "data/coinbase_products.csv"
    products_df = pd.DataFrame(json.loads(product_response.text), columns=product_columns).filter(items=['id','base_currency','quote_currency','status'])
    ## Filter our delisted currency products
    products_df = products_df[~products_df['status'].isin(['delisted'])]
    products_df = products_df.drop(columns=["status"])
    ## Save a local copy
    products_df.to_csv(filename, index=False)
    print(f"Created CSV file: {filename}")

    return products_df
