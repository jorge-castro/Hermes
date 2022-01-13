from json import dumps
import requests
import yfinance as yf


#Greet the user when they interact with the bot for the first time
def start():
    return "Hello! I'm Hermes, your new financial assistant."


#Show a help message to the user
def help():
    return "I'm a bot that can provide information on different financial " \
           "assets, i.e. the price of various cryptocurrencies and stocks.\n" \
           "Select a command to see usage examples."


#Queries the coingecko API and returns basic info on the coin(s)
def get_crypto_price(ids, vs_currencies="usd", include_market_cap="false",
                     include_24hr_vol="false", include_24hr_change="false",
                     include_last_updated_at="false"):
    
    r = requests.get(f"https://api.coingecko.com/api/v3/simple/price"
                     f"?ids={ids}"
                     f"&vs_currencies={vs_currencies}"
                     f"&include_market_cap={include_market_cap}"
                     f"&include_24hr_vol={include_24hr_vol}"
                     f"&include_24hr_change={include_24hr_change}"
                     f"&include_last_updated_at={include_last_updated_at}")

    return dumps(r.json(), indent=4)


#Takes a string of space-separated tickers and returns stock price(s) in the
#format "{ticker:market_price}"
def get_stock_price(tickers):
    stocks = yf.Tickers(tickers).tickers

    prices = {ticker: stock.info["regularMarketPrice"]
              for ticker, stock in stocks.items()
              if stock.info["regularMarketPrice"] != None}

    return dumps(prices, indent=4)


