#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Jascha van Zyl"
__version__ = "0.1.0"
__license__ = "MIT"

import pandas as pd
import numpy as np
import ccxt
from prettytable import PrettyTable
from datetime import datetime
import time


def fetch_ohlcv(symbol, time_frame='5m', days_back=365, lim=4896):
    ftx = ccxt.ftx({
        'enableRateLimit': True,
    })
    data = {
        "date": [],
        "open": [],
        "high": [],
        "low": [],
        "close": [],
        "volume": []
    }
    duration = ftx.parse_timeframe(time_frame) * 1000
    since = ftx.milliseconds() - (86400000 * days_back)
    if ftx.has['fetchOHLCV']:
        while since < ftx.milliseconds():
            time.sleep(0.5)
            ohlcv_piece = ftx.fetch_ohlcv(symbol,
                                          since=since,
                                          timeframe=time_frame,
                                          limit=lim)
            for data_piece in ohlcv_piece:
                data["date"].append(
                    datetime.fromtimestamp(
                        data_piece[0] /
                        1000.0).strftime('%Y-%m-%d %H:%M:%S.%f'))
                data["open"].append(data_piece[1])
                data["high"].append(data_piece[2])
                data["low"].append(data_piece[3])
                data["close"].append(data_piece[4])
                data["volume"].append(data_piece[5])
            if len(ohlcv_piece):
                last = ohlcv_piece[len(ohlcv_piece) - 1]
                since = last[0] + duration
            else:
                break
    data_frame = pd.DataFrame(data)
    return data_frame


def annual_sharpe_ratio(data_frame, n, rf):
    returns = data_frame['close'].pct_change()
    excess_returns = returns - rf / n
    mean = excess_returns.mean()
    sigma = returns.std()
    return (mean / sigma) * np.sqrt(n)


def annual_sortino_ratio(data_frame, n, rf):
    returns = data_frame['close'].pct_change()
    excess_returns = returns - rf / n
    mean = excess_returns.mean()
    std_neg = returns[returns < 0].std()
    return (mean / std_neg) * np.sqrt(n)


def information_ratio(returns, benchmark_returns, n):
    daily_returns = returns["close"].pct_change()
    daily_bench_returns = benchmark_returns["close"].pct_change()
    returns_return = np.prod(daily_returns + 1) - 1
    bench_return = np.prod(daily_bench_returns + 1) - 1
    diff = returns["close"].pct_change(
    ) - benchmark_returns["close"].pct_change()
    te = diff.std() * np.sqrt(n)
    return (returns_return - bench_return) / te


def full_tracking_error(returns, benchmark_returns, n):
    tracking_error = (returns["close"].pct_change() -
                      benchmark_returns["close"].pct_change()).std()
    return tracking_error * np.sqrt(n)


def rolling_tracking_error(returns, benchmark_returns, n):
    rolling = returns["close"].pct_change(
    ) - benchmark_returns["close"].pct_change()
    rolling = rolling[-n:]
    return rolling.std()


def main():
    """ Main entry point of the app """
    table_1 = PrettyTable()
    table_1.field_names = ["Symbol", "Sharpe Ratio", "Sortino Ratio"]
    symbols = ["BTC/USD", "ETH/USD", "BTC-PERP", "ETH-PERP"]
    all_ohlcv = []
    for symbol in symbols:
        fetched_ohlcv = fetch_ohlcv(symbol, time_frame='5m', days_back=365)
        all_ohlcv.append(fetched_ohlcv)
    for i in range(2):
        table_1.add_row([
            symbols[i],
            annual_sharpe_ratio(all_ohlcv[i], 105120, 0.0129),
            annual_sortino_ratio(all_ohlcv[i], 105120, 0.0129)
        ])

    table_2 = PrettyTable()
    table_2.field_names = ["BTC vs ETH Information Ratio"]
    table_2.add_row([information_ratio(all_ohlcv[0], all_ohlcv[1], 105120)])

    table_3 = PrettyTable()
    table_3.field_names = [
        "Symbols", "Full Tracking error", "Rolling 7 Day Tracking error"
    ]
    table_3.add_row([
        "BTC vs ETH-PERP",
        full_tracking_error(all_ohlcv[0], all_ohlcv[3], 105120),
        rolling_tracking_error(all_ohlcv[0], all_ohlcv[3], 2016)
    ])
    table_3.add_row([
        "ETH vs BTC-PERP",
        full_tracking_error(all_ohlcv[1], all_ohlcv[2], 105120),
        rolling_tracking_error(all_ohlcv[1], all_ohlcv[2], 2016)
    ])

    print(table_1)
    print(table_2)
    print(table_3)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
