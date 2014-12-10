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
        # If value fell below floor, sell all bitcoins!
        print('Floor breached, selling!')
        sell(current, log, account, currency='BTC')
        return 0
    elif target_investment > 0:
        if target_investment > current_currency:
            # Need to buy more
            print('Buying bitcoins worth $', target_investment - current_currency)
            buy(target_investment - current_currency, log, account, currency)
        elif current_currency > target_investment:
            # Need to sell off some bitcoins
            print('Selling bitcoins worth $', current_currency - target_investment)
            sell(current_currency - target_investment, log, account, currency)
        else:
            print('Sitting tight')
            write_str = time.strftime("%m.%d.%y %H:%M ", time.localtime())
            write_str += 'Target investment matches current investment \n'
            log.write(write_str.encode("utf-8"))
        return target_investment
    else:
        print('Sitting tight')
        write_str = time.strftime("%m.%d.%y %H:%M ", time.localtime())
        write_str += 'Target investment non-positive, current investment 0 \n'
        log.write(write_str.encode("utf-8"))
        return 0


def cppi_rebalance(portfolio_value, floor, interval, log, account, multiplier=3, currency='USD'):
    pvalue = portfolio_value
    while True:
        bitcoin_investment = cppi(pvalue, floor, log, account, multiplier, currency)
        cash = pvalue - bitcoin_investment
        time.sleep(interval)
        pvalue = cash + query(account) * exchange_rate(currency)


if __name__ == '__main__':
    my_account = list_accounts()
    tradelogs = input('Enter name of log file: ')
    log = open(tradelogs, 'wb', 0)
    interval = int(input('Time interval to rebalance portfolio (in seconds): '))
    currency = input('Enter currency: ')
    initial_pvalue = float(input('Initial value of portfolio (including bitcoin investments if any): '))
    floor = float(input('Enter floor: '))
    multiplier = float(input('Enter multiplier: '))
    cppi_rebalance(initial_pvalue, floor, interval, log, my_account[0], multiplier, currency)
