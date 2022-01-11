import requests
import yfinance as yf


#Greet the user when they interact with the bot for the first time
def start():
    return "Hello! I'm Hermes, your new financial assistant."


#Show a help message to the user
def help():
    return "I'm a bot that can provide the price of different financial assets"


#Queries the coingecko API and returns basic info on the coin(s) as
#deserialized json data
def get_crypto_price(ids="handshake", vs_currencies="usd", include_market_cap="false",
                     include_24hr_vol="false", include_24hr_change="false",
                     include_last_updated_at="false"):
    
    return requests.get(f"https://api.coingecko.com/api/v3/simple/price"
                        f"?ids={ids}"
                        f"&vs_currencies={vs_currencies}"
                        f"&include_market_cap={include_market_cap}"
                        f"&include_24hr_vol={include_24hr_vol}"
                        f"&include_24hr_change={include_24hr_change}"
                        f"&include_last_updated_at={include_last_updated_at}").json()


#Takes a str of space-separated tickers and returns stock price in the
#format {ticker:market_price}
def get_stock_price(tickers="MSFT GOOG"):
    stocks = yf.Tickers(tickers).tickers
    return {ticker: stock.info["regularMarketPrice"] for ticker, stock in stocks.items()}


#Takes a dict in the format {ticker:no_of_shares} and returns a dict
#containing {ticker:{no_of_shares:x, worth_of_shares:y}}
def get_worth_of_shares(shares={"MSFT":10}):
    prices = get_stock_price(" ".join(shares.keys()))
    return {ticker.upper(): {"no_of_shares": shares[ticker],
                             "worth_of_shares": shares[ticker]*prices[ticker.upper()]}
            for ticker in shares.keys()}


