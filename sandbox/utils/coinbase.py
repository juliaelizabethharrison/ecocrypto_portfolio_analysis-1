import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

cb_pro = os.getenv("COINBASE_PRO_FQDN")
cb_pub = os.getenv("COINBASE_PUB_FQDN")
cb_sandbox = os.getenv("COINBASE_SANDBOX_FQDN")

## Our coinbase Data Retrieval Library

def fetch_product_trades(product):
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
        
    return


# Fetch product ticker into dict()
def fetch_product_ticker(product):
    ticker_url = f"{cb_pub}/products/{product}/ticker"
    headers = {"Accept": "application/json"}
    response = requests.get(ticker_url, headers=headers)

    if response.status_code == 200:
        return dict(json.loads(response.text))
    else:
        print("Did not receieve OK response from Coinbase API")
       
    return

# Get a specific product stats
def fetch_product_stats(product):
    stats_url = f"{cb_pub}/products/{product}/stats"
    headers = {"Accept": "application/json"}
    response = requests.get(stats_url, headers=headers)

    if response.status_code == 200:
        return dict(json.loads(response.text))
    else:
        print("Did not receieve OK response from Coinbase API")
    return
