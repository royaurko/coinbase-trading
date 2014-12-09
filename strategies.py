#!/usr/bin/python3
import time
from trade import list_accounts, query, buy, sell, exchange_rate


# Constant proportion portfolio insurance - CPPI
# portfolio_value represents the value of your portfolio at a given time
# floor is the minimum value to which you are willing to let your portfolip drop
# multiplier is your sensitivity to risk
# A lower multiplier is more conservative, typically chosen between 3-6
def cppi(portfolio_value, floor, log, account, multiplier=3, currency='USD'):
    target_investment = multiplier * (portfolio_value - floor)
    current = query(account)
    current_currency = current * exchange_rate(currency)
    if target_investment < 0 and current_currency > 0:
        #If value fell below floor, sell all bitcoins!
        print('Floor breached, selling!')
        sell(current, log, account, currency='BTC')
        return 0
    elif target_investment > 0:
        if target_investment > current_currency :
            #Need to buy more
            print('Buying $', target_investment - current_currency)
            buy(target_investment - current_currency, log, account, currency)
        elif current_currency > target_investment:
            #Need to sell off some bitcoins
            print('Selling $', current_currency - target_investment)
            sell(current_currency - target_investment, log, account, currency)
        else:
            print('Sitting tight')
        return target_investment


def cppi_rebalance(portfolio_value, floor, interval, log, account, multiplier=3, currency='USD'):
    while True :
        bitcoin_investment = cppi(portfolio_value, floor, log, account, multiplier, currency)
        cash = portfolio_value - bitcoin_investment
        time.sleep(interval)
        portfolio_value = cash + query(account) * exchange_rate(currency)


if __name__ == '__main__':
    my_account = list_accounts()
    log = open('tradelogs', 'wb', 0)
    time_interval = 20
    initial_portfolio_value = 10
    initial_investment = 0
    cppi_rebalance(10, 9, 60, log, my_account[0], 3, 'USD')

