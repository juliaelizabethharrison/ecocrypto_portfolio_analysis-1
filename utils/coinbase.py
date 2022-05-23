import os
import glob
import fnmatch
import pandas as pd
import numpy as np
import time
import requests
import json
import warnings
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

"""
Utility library used to pull data from the Coinbase api

Requires:
- coinbase api key (not implimented)
- dotenv installed to read environment variables.

"""

## Coinbase Data Retrieval Library
cb_pro = os.getenv("COINBASE_PRO_FQDN")
cb_pub = os.getenv("COINBASE_PUB_FQDN")
cb_sandbox = os.getenv("COINBASE_SANDBOX_FQDN")

def sleep(t):
    time.sleep(t)
    return
    
def fetch_product_trades(product):
    """
    Saves local CSV file and returns a DataFrame object for product trades
    
    Input: String
    Returns: DataFrame for product trades
    
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
            filename = f'data/product/trades/coinbase_{product}_trades_{today}.csv'
            trades_df.to_csv(filename, index=False)
            print(f'Created CSV file: {filename}.')
    else:
        print("Did not receieve OK response from Coinbase API")
        print(response.text)
        
    return trades_df


def fetch_product_ticker(product):
    """
    Input: String
    Returns: json text response for product ticker header
    
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
    Input: String
    Returns: json text response for product stats header
    
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
    Input: String
    Returns: json text response for currencies
    
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
    Input: String
    Returns: json text response for products
    
    """    
    product_url = f"{cb_pub}/products"
    headers = {"Accept": "application/json"}
    product_response = requests.get(product_url, headers=headers)
    product_columns=["id","base_currency","quote_currency","base_min_size","base_max_size","quote_increment","base_increment","display_name","min_market_funds",
                     "max_market_funds","margin_enabled","fx_stablecoin","max_slippage_percentage","post_only","limit_only","cancel_only","trading_disabled","status","status_message","auction_mode"]
    
    # if product_response.status.code == 200:  NOTE:  This endpoint doesn't return a response code I think
    filename = "data/coinbase_products.csv"
    products_df = pd.DataFrame(json.loads(product_response.text), columns=product_columns) # .filter(items=['id','base_currency','quote_currency','status'])
    ## Filter our delisted currency products
    products_df = products_df[~products_df['status'].isin(['delisted'])]
    products_df = products_df.drop(columns=["status"])
    ## Save a local copy
    products_df.to_csv(filename, index=False)
    print(f"Created CSV file: {filename}")

    return products_df


def fetch_product_candles(product, gran, start, end):
   
    url = f'{cb_pub}/products/{product}/candles?granularity={gran}&start={start}&end={end}'
    response = requests.get(url)
    if response.status_code == 200:
        candles_df = pd.DataFrame(json.loads(response.text), columns=['unix', 'low', 'high', 'open', 'close', 'volume'])
        candles_df['date'] = pd.to_datetime(candles_df['unix'], unit='s')  # convert to a readable date
        candles_df['time'] = pd.to_datetime(candles_df['unix'], unit='s')
        candles_df['vol_fiat'] = candles_df['volume'] * candles_df['close'] # multiply the BTC volume by closing price to approximate fiat volume
        today = datetime.today().strftime('%Y-%m-%d')

        if candles_df is None:
            print("Did not return any data from Coinbase for this symbol")
        else:
            filename = f'data/product/candles/coinbase_{product}_candles_{end}.csv'
            candles_df.to_csv(filename, index=False)
            print(f'Created CSV file: {filename}.')
    else:
        print("Did not receieve OK response from Coinbase API")

    return candles_df


def subtract_days(date, days):
    subtracted_date = pd.to_datetime(date) - timedelta(days=days)
    subtracted_date = subtracted_date.strftime("%Y-%m-%d")
    return subtracted_date

def fetch_return_history(coin, date, seq):
    
    date = pd.to_datetime(date)    
    for num in seq:
        end_date=subtract_days(date, num)
        last_num=num+300
        start_date=subtract_days(datetime.today().strftime("%Y-%m-%d"), last_num)
        gran='86400'   # must be one of 60, 300, 900, 3600, 21600, 86400 seconds.
        print(f"Fetching data between: {start_date} and {end_date}.")
        
        # Now we make the actual request in another function
        fetch_product_candles(coin,gran,start_date,end_date)
        sleep(1) # snooze so we dont wake the dragons
    
    files = []
    for file in os.listdir("data/product/candles"):
        if os.path.getsize(f"data/product/candles/{file}") < 1 * 64:
            os.remove(f"data/product/candles/{file}")
            files.append(file)

    # print(f"{ len(files)} files < 1kb (no data) have been deleted")
    return None



def merge_candle_data(coin):
    
    files = []
    for file in os.listdir('data/product/candles'):     
        if fnmatch.fnmatch(file, f'*{coin}*'):
            files.append(file)
    
    # Must sort reverse because we're goin backwards in time. lol
    files.sort(reverse=True)
    list_iterator = iter(files)
    dis_df = pd.read_csv(Path(f"data/product/candles/{files[0]}"), infer_datetime_format=True, parse_dates=True)
    
    next(list_iterator)
    for file in list_iterator:
        # print(file)
        dat_df = pd.read_csv(Path(f"data/product/candles/{file}"), infer_datetime_format=True, parse_dates=True)
        joined_data = pd.concat([dis_df,dat_df], axis="rows", join="inner")
        dis_df = joined_data

    # dis_df = dis_df.set_index('date')
    joined_data = dis_df.sort_index(axis=1)

    filename = f'data/product/candles/merged/coinbase_{coin}_candles_ALL.csv'
    joined_data.to_csv(Path(filename))
    
    files_deleted = []
    for file in os.listdir("data/product/candles"):
        if fnmatch.fnmatch(file, f'*{coin}*'):
            os.remove(f"data/product/candles/{file}")
            files_deleted.append(file)
            
    print(f"Sucessfully merged {len(dis_df)} rows from {len(files)} files into the returned Dataframe.")

    return None



def get_merged_candle_data(coin):
    
#     files = []
#     for file in os.listdir('data/product/candles'):     
#         if fnmatch.fnmatch(file, f'*{coin}*'):
#             files.append(file)
    
#     # Must sort reverse because we're goin backwards in time. lol
#     files.sort(reverse=True)
#     list_iterator = iter(files)
#     dis_df = pd.read_csv(Path(f"data/product/candles/{files[0]}"), infer_datetime_format=True, parse_dates=True)
    
#     next(list_iterator)
#     for file in list_iterator:
#         # print(file)
#         dat_df = pd.read_csv(Path(f"data/product/candles/{file}"), infer_datetime_format=True, parse_dates=True)
#         joined_data = pd.concat([dis_df,dat_df], axis="rows", join="inner")
#         dis_df = joined_data

#     # dis_df = dis_df.set_index('date')
#     joined_data = dis_df.sort_index(axis=1)

#     filename = f'data/product/candles/merged/coinbase_{coin}_candles_ALL.csv'
#     joined_data.to_csv(Path(filename))
#     print(f"Sucessfully merged {len(dis_df)} rows from {len(files)} files into the returned Dataframe.")

    return joined_data


def get_portfolio_lists():
    
    # currencies_df = get_currencies()
    products_online_df = get_products()

    ## Filter by `base_currency` to get all crypto currencies by fiat `USD` and import into a DataFrame
    btc_usd_products_df = products_online_df.loc[(products_online_df['base_currency'] == 'BTC')&(products_online_df['quote_currency'] == 'USD')].copy().drop(columns=["quote_currency"])
    eth_usd_products_df = products_online_df.loc[(products_online_df['base_currency'] == 'ETH')&(products_online_df['quote_currency'] == 'USD')].copy().drop(columns=["quote_currency"])
    btc_products_df = products_online_df.loc[(products_online_df['quote_currency'] == 'BTC')].copy().drop(columns=["quote_currency"])
    eth_products_df = products_online_df.loc[(products_online_df['quote_currency'] == 'ETH')].copy().drop(columns=["quote_currency"])

    # Pandas concat() inner join into a list()
    pow_coins = pd.concat([btc_usd_products_df['id'],eth_usd_products_df['id']], join="inner").tolist()
    pos_coins = ["ADA-BTC","SOL-BTC","ALGO-BTC","XTZ-BTC"]
    
    return [pow_coins, pos_coins]

# Dataframes must be initialized within the runtime env
# def initialize_df_collection():
    
#     # Using glob functionality to grab the filenames of our merged data into a pandas dictionary
#     extension = 'csv'
#     files = glob.glob('data/product/candles/merged/*.{}'.format(extension))
#     file_dict = {}
#     for file in files:
#         key = file
#         df = pd.read_csv(file)
#         file_dict[key] = df

#     # Now rename our dataframes to prevent headaches:
#     btc_df = file_dict["data/product/candles/merged/coinbase_BTC-USD_candles_ALL.csv"].drop(columns=["Unnamed: 0","unix"]).set_index("time")
#     eth_df = file_dict["data/product/candles/merged/coinbase_ETH-USD_candles_ALL.csv"].drop(columns=["Unnamed: 0","unix"]).set_index("time")
#     ada_df = file_dict["data/product/candles/merged/coinbase_ADA-BTC_candles_ALL.csv"].drop(columns=["Unnamed: 0","unix"]).set_index("time")
#     sol_df = file_dict["data/product/candles/merged/coinbase_SOL-BTC_candles_ALL.csv"].drop(columns=["Unnamed: 0","unix"]).set_index("time")
#     algo_df = file_dict["data/product/candles/merged/coinbase_ALGO-BTC_candles_ALL.csv"].drop(columns=["Unnamed: 0","unix"]).set_index("time")
#     xtz_df = file_dict["data/product/candles/merged/coinbase_XTZ-BTC_candles_ALL.csv"].drop(columns=["Unnamed: 0","unix"]).set_index("time")

#     # Adding pct change to all df
#     btc_df["pct_change"] = btc_df["close"].pct_change().fillna(0) 
#     eth_df["pct_change"] = eth_df["close"].pct_change().fillna(0) 
#     ada_df["pct_change"] = ada_df["close"].pct_change().fillna(0) 
#     sol_df["pct_change"] = sol_df["close"].pct_change().fillna(0) 
#     algo_df["pct_change"] = algo_df["close"].pct_change().fillna(0)
#     xtz_df["pct_change"] = xtz_df["close"].pct_change().fillna(0)
    
#     return btc_df, eth_df, ada_df, sol_df, algo_df, xtz_df
