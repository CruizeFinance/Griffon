import requests


class TokenUtilities:
    def get_token_price_in_eth(token_ticker):

        if token_ticker != "USDT":
            while True:
                r = requests.get(
                    f"https://api.binance.com/api/v3/ticker/price?symbol={token_ticker}USDT"
                )
                if r.status_code == 200:
                    break
            data = r.json()
            token_in_usdt = float(data["price"])
        else:
            token_in_usdt = 1.0

        while True:
            r = requests.get(
                "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"
            )
            if r.status_code == 200:
                break
        data = r.json()
        eth_in_usdt = float(data["price"])

        return token_in_usdt / eth_in_usdt
