#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Jascha van Zyl"
__version__ = "0.1.0"
__license__ = "MIT"

import json
import sys


class CapitalAllocator(object):
    def __init__(self, account_name, old_allocation_fraction,
                 new_allocation_fraction):
        super(CapitalAllocator, self).__init__()
        self.account_name = account_name
        self.old_allocation_fraction = old_allocation_fraction
        self.new_allocation_fraction = new_allocation_fraction
        self.allocation_difference = self.old_allocation_fraction - \
            self.new_allocation_fraction

    def subtract_allocation(self, allocation_fraction):
        self.allocation_difference -= allocation_fraction

    def add_allocation(self, allocation_fraction):
        self.allocation_difference += allocation_fraction

    def has_excess_allocation_available(self):
        return round(self.allocation_difference, 6) > 0

    def has_excess_allocation_required(self):
        return round(self.allocation_difference, 6) < 0

    def get_excess_required(self):
        return round(-1 * self.allocation_difference, 6)

    def get_excess_available(self):
        return round(self.allocation_difference, 6)

    def get_excess_shiftable(self, excess_available, excess_required):
        if excess_required > excess_available:
            return excess_available
        elif excess_required <= excess_available:
            return excess_required

    def shift_allocations(self, capital_allocators):
        allocation_shifts = []
        for other_account in capital_allocators:
            if self.has_excess_allocation_available(
            ) and other_account.has_excess_allocation_required():
                excess_shiftable = self.get_excess_shiftable(
                    self.get_excess_available(),
                    other_account.get_excess_required())
                self.subtract_allocation(excess_shiftable)
                other_account.add_allocation(excess_shiftable)
                allocation_shifts.append({
                    "excess_shiftable": excess_shiftable,
                    "from": self.account_name,
                    "to": other_account.account_name
                })
        return allocation_shifts


def load_inputs(inputfile):
    with open(inputfile) as json_file:
        input_values = json.load(json_file)
        json_file.close()
    total_capital = input_values["total_capital"]
    accounts = input_values["accounts"]
    return total_capital, accounts


def check_valid_input(accounts):
    # Should add up to 2 for fraction allocations to balance
    total_fraction_allocations = round(
        sum(
            map(
                lambda account: account["old_allocation_fraction"] + account[
                    "new_allocation_fraction"], accounts)), 2)
    if total_fraction_allocations == 2:
        return True
    else:
        return False


def create_allocation_objects(accounts):
    capital_allocations = []
    for account in accounts:
        account_to_add = CapitalAllocator(account["account_name"],
                                          account["old_allocation_fraction"],
                                          account["new_allocation_fraction"])
        capital_allocations.append(account_to_add)
    return capital_allocations


def calculate_allocation_shifts(capital_allocations, total_capital):
    unfiltered_output = []
    for capital_allocator in capital_allocations:
        unfiltered_output.append(
            capital_allocator.shift_allocations(capital_allocations))
    # Remove empty [] entries in list
    filtered_output = [
        allocation_shift for sublist in unfiltered_output
        for allocation_shift in sublist
    ]
    # Format final output for display
    final_output = [
        "Send {} to {} from {}".format(
            round(allocation_shift["excess_shiftable"] * total_capital, 2),
            allocation_shift["from"], allocation_shift["to"])
        for allocation_shift in filtered_output
    ]
    return final_output


def main():
    """ Main entry point of the app """
    # Try load input values
    try:
        total_capital, accounts = load_inputs("inputs.json")
    except:
        print("'inputs.json' not found.")
        sys.exit(1)
    # Check valid input and continue
    if check_valid_input(accounts):
        capital_allocations = create_allocation_objects(accounts)
        # Calculate allocation shifts and print results
        print(calculate_allocation_shifts(capital_allocations, total_capital))
    else:
        print("Allocation fractions do not add up to valid amount.")


if __name__ == "__main__":
    main()
