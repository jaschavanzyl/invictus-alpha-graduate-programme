<h2 align="center">Invictus Alpha Graduate Program Quantitative Assessment</h2>

## Question 1 - Theory
<p align="justify">
  
**1.1.1)** Transactions are calculated based on gas (the number of computations that have to be done to complete the transaction), gas limit (maximum gas the user is willing to use per transaction) and the gas price (how much a user is willing to pay per gas of work done, usually denoted in Gwei). Transaction cost is then calculated as: transaction cost = gas price * gas used.  Gas limit is a constant user defined variable were gas is a constant determined by the number of computations per transaction. Acceptable gas prices can vary based on network congestion, the users’ gas price has to be within an acceptable range for the transaction to be executed, if the network is congested the price per computation increases and therefor the acceptable gas price increases. Transaction costs can also increase due to an increase in the ETH/USD exchange rate, as Ethereum becomes more valuable the dollar amount per transaction will increase.

**1.1.2)** When processing any transaction there will be a fee, fee’s will need to be taken into account when deciding at which price to execute, as fees can cause a trade that seems profitable to incur a loss. Trading quantity and frequency will also affect the amount of fees you incur when trading as most exchanges charge lower fees for higher trade volumes. Frequent trading will incur more fees, combined with small volume trades, the effect will be amplified and a lot of the traders profit will be payed away in fees. Time of day will also play a role in the transaction cost, as with ETH, the network might be more congested later in the day and a higher fee will be charged to process the transaction. Taking all this into account, less frequent trading with high volume implemented on a buy and hold strategy is one way of eliminating some of the fees.  

**1.1.3)** Automated market makers are part of the decentralized finance ecosystem, they allow the trade of digital assets automatically by using a liquidity pool rather than relying on buyer and seller interactions. Automated market makers are also not owned by a single entity. On a regular exchange, the exchange matches bids and offers, there for a trade cannot be executed if a buyer and seller cannot be matched as regular exchanges do not use an liquidity pool, there are also owned by a single entity. 

**1.1.4)** Flash loans are instant with no limit on the loan amount and no requirement of collateral or credit checks. These loans are guaranteed by the fact that the loan and the repayment of the loan have to occur in the same transaction otherwise the transaction is reversed.

**1.2)** Stable coins are cryptocurrencies were the value of the cryptocurrency is pegged to an asset, e.g. fiat money or exchange-traded commodities. They can be collateralized or non-collateralized (algorithmic). Cryptocurrencies are often unpredictable and fluctuate widely, stable coins lessen these fluctuations by pegging the coin to a more stable asset e.g. the US dollar. Stable coins can be collateralized or non-collateralized, collateralized stable coins can be constructed by pegging the value of the coin to a currency, backing the coin with assets other than fiat or cryptocurrencies or by backing the coins with cryptocurrencies. Non-collateralized stable coins are backed by an algorithm that determines the price of the currency by looking at demand and supply. Another method of constructing stable coins is the hybrid method, these coins are collateralized by one of the above mentioned methods, but also modelled algorithmically, which is the non-collateralized portion.

**1.3)** A perpetual future is a future to non-optionally buy or sell an asset at an unspecified future date. They can be held indefinitely which eliminates the need for roll overs. If a person buys `x` amount of bitcoin in the spot market and at the same time shorts `x` amount of bitcoin on a perpetual future their position is market neutral, they will however still receive the funding rate at pre-determined time intervals depending on the futures price vs the index price, this in turn creates an arbitrage opportunity which is created by the futures price converging to zero on a regular basis.
</p>

## Getting Started - Question 2, 3 and 4

## Project Scaffolding
```
jaschavanzyl/invictus-alpha-graduate-programme
├── Images
│   ├── question3-image1.png
│   ├── question3-image2.png
│   └── question3-image3.png
├── Question2.1
│   ├── inputs.json
│   └── main.py
├── Question2.2
│   ├── inputs.json
│   └── main.py
├── Question3
│   └── main.py
├── Question4
│   └── main.py
└── requirements.txt

```

### Prerequisites
Please ensure you have the latest version of Python installed on your operating system. The steps for installing Python for your operating system can be found on the [official website](https://www.python.org/). 
### Installation
Before attempting to execute any of the Python code, please ensure that the respective Python packages required to successfully run the code has been installed by firstly navigating to the root of the project where `requirements.txt` is located, and then running the following command:

 ```sh
  pip install -r requirements.txt
  ```
  ## Usage
  ### Question 2.1
  * Navigate to `Question2.1/`
  * Please ensure that `inputs.json` is located in the same directory as `main.py`
  * Run `python main.py` from within the same folder where `inputs.json` and `main.py` are located
  * Monitor the terminal for output

### Question 2.2
  * Navigate to `Question2.2/`
  * Please ensure that `inputs.json` is located in the same directory as `main.py`
  * Run `python main.py` from within the same folder where `inputs.json` and `main.py` are located
  * Monitor the terminal for output

### Question 3
  * Navigate to `Question3/`
  * Run `python main.py` from within the same folder where `main.py` is located
  * Please wait a few minutes for the program to finish execution
  * Monitor the terminal for output

### Question 4
  * Navigate to `Question4/`
  * Run `python main.py` from within the same folder where `main.py` is located
  * Please wait a few minutes for the program to finish execution
  * Monitor the terminal for output as well as the respective files named `balance.csv`, `filled_orders.csv` and `open_orders.csv` which will be created in the same directory of execution
  * NOTE: To stop execution, pass a keyboard interrupt (`ctrl + c` or `cmd + c`) to the terminal

## Supporting Documentation

### Question 2.1 - Python Documentation
The program reads input values from a JSON file with the following strucuture:

``` JSON
{
    "total_capital": 2100,
    "accounts": [
        {
            "account_name": "Arbitrage",
            "old_allocation_fraction": 0.476190,
            "new_allocation_fraction": 0.3
        },
        {
            "account_name": "Quant",
            "old_allocation_fraction": 0.238095,
            "new_allocation_fraction": 0.5
        },
        {
            "account_name": "Discretionary",
            "old_allocation_fraction": 0.285714,
            "new_allocation_fraction": 0.1
        },
        {
            "account_name": "SEC Fines",
            "old_allocation_fraction": 0.0,
            "new_allocation_fraction": 0.1
        }
    ]
}
```
Once the respective fields have been read, the program ensures that the inputs are valid by adding up the fields of `old_allocation_fraction` and `new_allocation_fraction` for each element in the `accounts` array. If the sum of both `old_allocation_fraction` and `new_allocation_fraction` from each array do not add up to `1` and `1` respectively, the user will be notified of the error. 

Assuming that the inputs are error free, the program will proceed to create a `CapitalAllocator` object for each of the `accounts` which has the member fields `account_name`, `old_allocation_fraction`, `new_allocation_fraction` and `new_allocation_difference`- which is calculated by subtracting `new_allocation_difference` from `old_allocation_difference`.

After these `CapitalAllocator` objects are created, each object is tested against the entire collection of objects to determine which allocation shifts need to be made. When a `CapitalAllocator` object has an __excess__ allocation available whilst its respective peer has an allocation __requirement__, the object will shift either its full __excess__ to the peer, or the exact amount required.

Once this process has finished, the program will print its output to the terminal.


### Question 2.2 - Python Documentation

The program reads input values from a JSON file with the following strucuture:

``` JSON
{
    "total_asset_cap": 0.5,
    "total_capital": 1000,
    "in_df": [
        {
            "ticker": "BTC",
            "market_cap": 20000,
            "price": 50
        },
        {
            "ticker": "ETH",
            "market_cap": 10000,
            "price": 25
        },
        {
            "ticker": "LTC",
            "market_cap": 5000,
            "price": 10
        }
    ]
}
```

The program then calculates the asset cap when each ticker is equally weighted by dividing one by the amount of tickers (`check_weight`). It then calculates the current index weight for each instrument and does a check to see if the desired asset cap is bigger than the `check_weight` and if there are any instruments that have a higher weight than the desired asset cap. If true, the instrument is downscaled to the desired asset cap and assigned a `True` value for `adjusted_cap` and a `False` value for `check_weight`. 

When the desired asset cap is smaller than the `check_weight` the instruments are all set to the `check_weight`, ensuring that they are equally weighted, else they keep their original index weight. The program then subtracts the number of instruments downscaled multiplied by the desired asset cap from the total asset cap and stores it as `adjusted_market_cap`. The remaining instruments are the re-weighted using the `remaining_market_cap` of each instrument divided by the sum of the `remaining_market_cap` of all remaining instruments. The new weight is then multiplied by the `adjusted_market_cap` and divided by the original total market cap to obtain each remaining instruments new index weight. The results are then printed out in a table format.

### Question 3 - Python Documentation

The program fetches the 5 minute interval OHCLV data for the past year from FTX using the `ccxt` Python package. Since FTX only allows a user to pull a certain amount of data at any given time, the program needs to send multiple request. During this period, the program will append the data received data from each request to a Pandas `data_frame` variable. Once the desired length is satisfied, the program will continue execution.

The **Sharpe ratio** is calculated by taking the percentage change of closing prices and subtracting the risk-free rate divided by `n ( n = days in a year * number of 5 minutes in a day)`. The program then calculates the mean of the result as well as the standard deviation of the percentage changes prior to subtracting the risk-free rate. This mean is the divided by the standard deviation and the result is multiplied by the square root of `n`, which annualizes the data.


The **Sortino** ratio is calculated in exactly the same manner as the **Sharpe** ratio above, except the standard deviation is only calculated using values less than zero as Sortino only factors in downside risk, the final result is also annualized.

The program calculates the difference between the portfolio return and benchmark return by taking the percentage change on the closing prices of each and adding one to find the cumulative product and then subtracting one for both the benchmark and the portfolio. The **tracking error** is then calculated by taking the percentage on the closing prices of both the benchmark and the portfolio and subtracting the benchmark changes from the portfolio changes and taking the standard deviation of the result. The standard deviation is then multiplied by the square root of `n (n = days * number of 5 minutes in a day)` to annualize the result. Finally the difference of the cumulative product of the benchmark return is subtracted from the portfolio return and the result is divided the annualized standard deviation (due to the fact that tracking error is the standard deviation of the differences) to obtain the **information ratio**.

The **full tracking error** is calculated by taking the percentage change of the closing prices of the portfolio and the benchmark and subtracting the percentage change of the benchmark from the percentage change of the portfolio. I then takes the standard deviation of the results and multiplies it by the square root of n (n=days*number of 5 minutes in a day) to obtain the annualized tracking error over the full series.

The **rolling tracking error** is calculated similar to the full tracking error except that after the benchmark percentage change has been subtracted from the portfolio percentage change the program takes the last `n ( n = number of 5 minutes in a day * number of days = 288 * 7 = 2016)` values and calculates the standard deviation of these values. In this case the result was left unchanged, it could however be multiplied by the square root of n for a better comparison to the annualized full tracking error.

### Question 3 - Analysis

**3.1)** From the below data it is clear that both BTC/USD and ETH/USD are good investment choices as the high sharpe ratios indicate a great risk adjusted return. The sortino ratio shows risk adjusted return based on downside risk, from the below data it is clear that both ETH and BTC have great risk adjusted returns when it comes to downside risk. Comparing the sharpe and sortino ratios of BTC and ETH it is clear that ETH has been the better investment over the past year, not only does it have a better risk adjusted return, but also has less downside risk.

The below calculations were made using a risk-free rate of 1.29%, the US 10 year treasury rate at the time of calculation.

<p align="center">
<img src="https://github.com/jaschavanzyl/invictus-alpha-graduate-programme/blob/2015ebbcd0110b1abf10c1fea44629f820856176/Images/question3-image1.png">
</p>

**3.2)** Looking at the below negative information ratio it is clear that BTC was not able to outperform the benchmark (ETH) the past year, this agrees with the ratios calculated in question 3.1.

<p align="center">
<img src="https://github.com/jaschavanzyl/invictus-alpha-graduate-programme/blob/2015ebbcd0110b1abf10c1fea44629f820856176/Images/question3-image2.png">
</p>

**3.3)** A high tracking error can point to both poor and good performance of a portfolio. In the case of BTC vs ETH-PERP, looking at question 3.1 and 3.3, it is clear that the high tracking error corresponds to poor performance as BTC is consistently underperforming against ETH-PERP over the course of a year. In the case of ETH vs BTC-PERP, it can be seen from question 3.1 and 3.2 that the high tracking error corresponds to good performance as ETH is consistently outperforming BTC-PERP over the course of year.

<p align="center">
<img src="https://github.com/jaschavanzyl/invictus-alpha-graduate-programme/blob/2015ebbcd0110b1abf10c1fea44629f820856176/Images/question3-image3.png">
</p>

### Question 4 - Python Documentation

The program will start by making use of the `cctx` Python package to form a connection to the Coinbase Pro Sandbox trading environment. Once this connection has been sucessfully formed, the program will fall into a perpetual loop of trading randomly. 

This process is described by the following steps:
<ol>
<li>The program randomly determines which market action to take:
  <ol>
  <li>
    If the program decides to place a buy order, it will either place a limit buy order based on a small percentage change in the base price, or place an instant market buy order by virtue of a random amount chosen between the minimum buy amount and the amount of USD funds available
    </li>
    <li>
      If the program decides to place a sell order, it will either place a limit sell order based on a small percentage change in the base price, or place an instant market sell order by virtue of a random amount chosen between the minimum sell amount and the amount of BTC funds available
    </li>
    <li>
      If the program decides to cancel open orders, it will do so by randomly selecting an open buy/sell order and requesting cancellation
    </li>
  </ol>
  </li>
<li>Once a market action has completed, the program will log the total balance available, the open buy/sell orders as well as the filled orders to their respective CSV files</li>
</ol>
