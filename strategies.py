#!/usr/bin/python3
from trade import list_accounts, query, buy, sell, status

# Constant proportion portfolio insurance - CPPI
# portfolio_value represents the value of your portfolio at a given time
# floor is the minimum value to which you are willing to let your portfolip drop
# multiplier is your sensitivity to risk
# A lower multiplier is more conservative, typically chosen between 3-6
def cppi(portfolio_value, floor, current_investment, log, account, multiplier='3', currency='USD'):
    target_investment = multiplier * (portfolio_value - floor)
    if target_investment < 0 and current_investment > 0:
        sell(current_investment, log, account, currency)
    elif target_investment > 0:
        if target_investment > current_investment:
            buy(target_investment - current_investment, log, account, currency)
        elif current_investment > target_investment:
            sell(current_investment-target_investment, log, account, currency)


if __name__ == '__main__':
    my_account = list_accounts()
    log = open('tradelogs', 'w')
    cppi(10, 9, 0, log, my_account[0], 5)
