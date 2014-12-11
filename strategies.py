#!/usr/bin/python3
import time
from trade import list_accounts, query, buy, sell, exchange_rate


# Constant proportion portfolio insurance - CPPI
# portfolio_value represents the value of your portfolio at a given time
# floor is the minimum value to which you are willing to let your portfolio drop
# multiplier is your sensitivity to risk
# A lower multiplier is more conservative, typically chosen between 3-6
def cppi(portfolio_value, floor, current_invested, log, account, multiplier=3, currency='USD', flag='n'):
    target_investment = multiplier * (portfolio_value - floor)
    if flag =='y':
        current = query(account)
        current_currency = current * exchange_rate(currency)
    else:
        current_currency = current_invested
    if target_investment < 0 and current_currency > 0:
        # If value fell below floor, sell all bitcoins!
        print('Floor breached, selling!')
        sell(current, log, account, 'BTC', flag)
        return 0
    elif target_investment > 0:
        # Coinbase allows buying only in units bigger than 1
        if target_investment > current_currency and target_investment - current_currency >= 1:
            # Need to buy more
            print('Buying bitcoins worth $', target_investment - current_currency)
            buy(target_investment - current_currency, log, account, currency, flag)
            write_str = ', Value of portfolio: ' + str(portfolio_value) + ' ' + currency + '\n'
            log.write(write_str.encode("utf-8"))
        elif current_currency > target_investment:
            # Need to sell off some bitcoins
            print('Selling bitcoins worth $', current_currency - target_investment)
            sell(current_currency - target_investment, log, account, currency, flag)
            write_str = ', Value of portfolio: ' + str(portfolio_value) + ' ' + currency + '\n'
            log.write(write_str.encode("utf-8"))
        else:
            print('Sitting tight')
            write_str = time.strftime("%m.%d.%y %H:%M ", time.localtime())
            write_str += 'Target investment of ' + str(target_investment) + ' matches current investment '
            write_str += ', Value of portfolio: ' + str(portfolio_value) + ' ' + currency + '\n'
            log.write(write_str.encode("utf-8"))
        return target_investment
    else:
        print('Sitting tight')
        write_str = time.strftime("%m.%d.%y %H:%M ", time.localtime())
        write_str += 'Target investment non-positive, current investment 0 '
        write_str += ', Value of portfolio: ' + portfolio_value + ' ' + currency + '\n'
        log.write(write_str.encode("utf-8"))
        return 0


def cppi_rebalance(portfolio_value, floor, current_invested, interval, log, account, multiplier=3, currency='USD', flag='n'):
    pvalue = portfolio_value
    while True:
        bitcoin_investment = cppi(pvalue, floor, current_invested, log, account, multiplier, currency, flag)
        old_rate = exchange_rate(currency)
        cash = pvalue - bitcoin_investment
        time.sleep(interval)
        if flag == 'y':
            pvalue = cash + query(account) * exchange_rate(currency)
        else:
            pvalue = cash + (bitcoin_investment/old_rate) * exchange_rate(currency)
            current_invested = (bitcoin_investment/old_rate) * exchange_rate(currency)


if __name__ == '__main__':
    my_account = list_accounts()
    flag = input('Real trade (Anything other than y implies simulation) [y/n]?: ')
    tradelogs = input('Enter name of log file: ')
    log = open(tradelogs, 'wb', 0)
    interval = int(input('Time interval to rebalance portfolio (in seconds): '))
    currency = input('Enter currency: ')
    initial_pvalue = float(input('Initial value of portfolio (including bitcoin investments if any): '))
    if flag == 'y':
        current_invested = query(account) * exchange_rate(currency)
    else:
        current_invested = float(input('Amount in ' + currency + ' currently invested in bitcoins: '))
    floor = float(input('Enter floor: '))
    multiplier = float(input('Enter multiplier: '))
    cppi_rebalance(initial_pvalue, floor, current_invested, interval, log, my_account[0], multiplier, currency, flag)
