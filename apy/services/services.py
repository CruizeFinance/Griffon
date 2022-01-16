import requests


class Services(object):
    def __init__(self, token):
        self.token = token

    def token_price(self):
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={self.token}USDT"
        request = requests.get(url)
        data = request.json()
        return data
