import requests


class Services(object):
    def __init__(self, token, token_ticker):
        self.token = token
        self.token_ticker = token_ticker

    def token_price(self):
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={self.token}{self.token_ticker}"
        request = requests.get(url)
        data = request.json()
        return data
