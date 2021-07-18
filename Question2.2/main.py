#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Jascha van Zyl"
__version__ = "0.1.0"
__license__ = "MIT"

import json
import sys
from prettytable import PrettyTable


def load_inputs(inputfile):
    with open(inputfile) as json_file:
        input_values = json.load(json_file)
        json_file.close()
    total_asset_cap = input_values["total_asset_cap"]
    total_capital = input_values["total_capital"]
    in_df = input_values["in_df"]
    return total_asset_cap, total_capital, in_df


def calculate_results(in_df, total_asset_cap, total_capital):
    ticker_amount = len([x["ticker"] for x in in_df])
    check_weight = 1 / ticker_amount
    market_capital_total = sum([x["market_cap"] for x in in_df])
    adjusted_instruments = 0
    for instrument in in_df:
        index_weight = (instrument["market_cap"] / market_capital_total)
        if index_weight > total_asset_cap > check_weight:
            instrument["index_weight"] = total_asset_cap
            instrument["adjusted_cap"] = True
            instrument["checked_weight"] = False
            adjusted_instruments += total_asset_cap
        elif total_asset_cap < check_weight:
            instrument["index_weight"] = check_weight
            instrument["adjusted_cap"] = False
            instrument["checked_weight"] = True
        else:
            instrument["index_weight"] = index_weight
            instrument["adjusted_cap"] = False
            instrument["checked_weight"] = False

    adjusted_market_cap = market_capital_total - \
        adjusted_instruments * market_capital_total
    remaining_market_cap = sum(
        [x["market_cap"] for x in in_df if x["adjusted_cap"] == False])
    for instrument in in_df:
        if not instrument["adjusted_cap"] and not instrument["checked_weight"]:
            instrument["index_weight"] = (
                (instrument["market_cap"] / remaining_market_cap) *
                adjusted_market_cap) / market_capital_total
        instrument["usd_value"] = instrument["index_weight"] * \
            total_capital
        instrument["amount"] = instrument["usd_value"] / instrument["price"]

    return in_df


def format_results(in_df):
    table = PrettyTable()
    table.field_names = ["Ticker", "Amount", "USD Value", "Percentage"]
    for instrument in in_df:
        table.add_row([
            instrument["ticker"],
            round(instrument["amount"], 2),
            round(instrument["usd_value"], 2),
            round(instrument["index_weight"] * 100, 4)
        ])
    return table


def main():
    """ Main entry point of the app """
    try:
        total_asset_cap, total_capital, in_df = load_inputs("inputs.json")
        in_df = calculate_results(in_df, total_asset_cap, total_capital)
        print(format_results(in_df))
    except:
        print("'inputs.json' not found.")
        sys.exit(1)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
