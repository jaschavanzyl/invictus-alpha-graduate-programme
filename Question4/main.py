#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Jascha van Zyl"
__version__ = "0.1.0"
__license__ = "MIT"

import ccxt
from datetime import datetime
import pandas as pd
import time
import random
from random import randrange


class CoinbaseProSandbox:
    def __init__(self, coin_base_pro_sandbox_object):
        self.coin_base_pro_sandbox_object = coin_base_pro_sandbox_object
        self.usd_balance = 0
        self.btc_balance = 0
        self.btc_price = 0
        self.open_order_ids = set()
        self.open_orders = {}
        self.filled_orders = {}
        self.all_balance = {}

    def trade_randomly(self):
        self.fetch_balance_values()
        trade_condition = randrange(2)
        order_has_limits = bool(random.getrandbits(1))
        if trade_condition == 0:
            amount = random.uniform(0.001, self.btc_balance)
            price = self.btc_price * \
                (random.uniform(0.04, 0.07) + 1)
            print(
                "Selling {} BTC at {} BTC/USD \nBalance Before Trade:\n USD balance: {} | BTC balance: {}"
                .format(amount, self.btc_price, self.usd_balance,
                        self.btc_balance))
            if order_has_limits:
                print("Limit : {}".format(price))
                self.create_sandbox_sell_limit_order(amount, price)
            else:
                self.create_sandbox_sell_order(amount)
        elif trade_condition == 1:
            amount = random.uniform(0.001, (self.usd_balance / self.btc_price))
            price = abs(self.btc_price * (random.uniform(0.04, 0.07) - 1))
            print(
                "Buying {} BTC at {} BTC/USD \nBalance Before Trade:\n USD balance: {} | BTC balance: {}"
                .format(amount, self.btc_price, self.usd_balance,
                        self.btc_balance))
            if order_has_limits:
                print("Limit : {}".format(price))
                self.create_sandbox_limit_order(amount, price)
            else:
                self.create_sandbox_sell_order(amount)
            self.create_sandbox_order(amount)
        elif trade_condition == 3:
            id = random.sample(self.open_order_ids, 1)
            print("Closing order with ID: {}".format(id))
            self.close_sandbox_order(id)

    def fetch_balance_values(self):
        markets = self.coin_base_pro_sandbox_object.fetch_markets()
        for market in markets:
            if market["symbol"] == "BTC/USD":
                btc_ticker = self.coin_base_pro_sandbox_object.fetch_ticker(
                    market["symbol"])
                self.btc_price = (float(btc_ticker['info']["ask"]) +
                                  float(btc_ticker["info"]["bid"])) / 2
        fetched_balance = self.coin_base_pro_sandbox_object.fetch_balance()
        self.usd_balance = fetched_balance["total"]["USD"]
        self.btc_balance = fetched_balance["total"]["BTC"]

    def close_sandbox_order(self, id):
        self.coin_base_pro_sandbox_object.cancel_order(id)

    def create_sandbox_order(self, amount, symbol="BTC/USD"):
        self.coin_base_pro_sandbox_object.create_market_buy_order(
            symbol, amount)

    def create_sandbox_sell_order(self, amount, symbol="BTC/USD"):
        self.coin_base_pro_sandbox_object.create_market_sell_order(
            symbol, amount)

    def create_sandbox_limit_order(self, amount, price, symbol="BTC/USD"):
        self.coin_base_pro_sandbox_object.create_limit_buy_order(
            symbol, amount, price)

    def create_sandbox_sell_limit_order(self, amount, price, symbol="BTC/USD"):
        self.coin_base_pro_sandbox_object.create_limit_sell_order(
            symbol, amount, price)

    def fetch_sandbox_balance(self):
        fetched_balance = self.coin_base_pro_sandbox_object.fetch_balance()
        formatted_balance = {}
        formatted_balance["free"] = fetched_balance["free"]
        formatted_balance["used"] = fetched_balance["used"]
        formatted_balance["total"] = fetched_balance["total"]
        formatted_balance["timestamp"] = datetime.fromtimestamp(
            self.coin_base_pro_sandbox_object.milliseconds() /
            1000.0).strftime('%Y-%m-%d %H:%M:%S.%f')
        self.all_balance = {
            "Symbol": [],
            "Free": [],
            "Used": [],
            "Total": [],
            "Timestamp": []
        }
        for symbol in formatted_balance["total"]:
            if symbol == "USD" or symbol == "BTC":
                self.all_balance["Symbol"].append(symbol)
                self.all_balance["Free"].append(
                    formatted_balance["free"][symbol])
                self.all_balance["Used"].append(
                    formatted_balance["used"][symbol])
                self.all_balance["Total"].append(
                    formatted_balance["total"][symbol])
                self.all_balance["Timestamp"].append(
                    formatted_balance["timestamp"])
            if symbol == "USD":
                self.usd_balance = formatted_balance["total"][symbol]
            elif symbol == "BTC":
                self.btc_balance = formatted_balance["total"][symbol]
        return self.all_balance

    def fetch_sandbox_open_orders(self, symbol="BTC/USD"):
        orders = self.coin_base_pro_sandbox_object.fetch_open_orders(
            symbol=symbol)
        self.open_orders = {
            "Symbol": [],
            "Side": [],
            "Size (USD)": [],
            "Price (USD)": [],
            "Fee (USD)": [],
            "Settled": [],
            "Timestamp": []
        }
        for order in orders:
            self.open_order_ids.add(order["id"])
            self.open_orders["Symbol"].append(order["symbol"]),
            self.open_orders["Side"].append(order["info"]["side"])
            self.open_orders["Size (USD)"].append(order["info"]["size"])
            self.open_orders["Price (USD)"].append(order["info"]["price"])
            self.open_orders["Fee (USD)"].append(order["fee"]["cost"])
            self.open_orders["Settled"].append(order["info"]["settled"])
            self.open_orders["Timestamp"].append(order["datetime"])
        return self.open_orders

    def fetch_sandbox_filled_orders(self, symbol="BTC/USD"):
        orders = self.coin_base_pro_sandbox_object.fetch_my_trades(
            symbol=symbol)
        self.filled_orders = {
            "Symbol": [],
            "Side": [],
            "Size (BTC)": [],
            "Price (USD)": [],
            "Fee (USD)": [],
            "Volume (USD)": [],
            "Settled": [],
            "Timestamp": []
        }
        for order in orders:
            self.filled_orders["Symbol"].append(order["symbol"])
            self.filled_orders["Side"].append(order["info"]["side"])
            self.filled_orders["Size (BTC)"].append(order["info"]["size"])
            self.filled_orders["Price (USD)"].append(order["info"]["price"])
            self.filled_orders["Fee (USD)"].append(order["fee"]["cost"])
            self.filled_orders["Volume (USD)"].append(
                order["info"]["usd_volume"])
            self.filled_orders["Settled"].append(order["info"]["settled"])
            self.filled_orders["Timestamp"].append(order["datetime"])
        return self.filled_orders

    def write_data_to_csv(self):
        pd.DataFrame(self.all_balance).to_csv("balance.csv")
        pd.DataFrame(self.filled_orders).to_csv("filled_orders.csv")
        pd.DataFrame(self.open_orders).to_csv("open_orders.csv")


def main():
    """ Main entry point of the app """
    coin_base_pro_sandbox_object = ccxt.coinbasepro({
        "apiKey": "ea8949a026125fa560724021efa4221b",
        "secret":
        "YU56ViylXvWzHhYvwHj54ak0GMnZkh23tGASEYO3iFIwD74O5pzJ7mfM4HpQ8KZixd5Biaf58NPA7pYQhtChPQ==",
        "password": "5uyh5r0pnzl",
        'enableRateLimit': True,
    })
    coin_base_pro_sandbox_object.set_sandbox_mode(enabled=True)
    coin_base_pro_sandbox = CoinbaseProSandbox(coin_base_pro_sandbox_object)
    while True:
        try:
            coin_base_pro_sandbox.trade_randomly()
            print("Trade successfully placed.")
            time.sleep(15)
            coin_base_pro_sandbox.fetch_sandbox_balance()
            coin_base_pro_sandbox.fetch_sandbox_filled_orders()
            coin_base_pro_sandbox.fetch_sandbox_open_orders()
            coin_base_pro_sandbox.write_data_to_csv()
            time.sleep(120)

        except:
            print("Trade failed, retrying...")
            time.sleep(15)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
