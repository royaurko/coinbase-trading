#!/usr/bin/python3
from trade import list_accounts, query, buy, sell, status


if __name__ == '__main__':
    my_account = list_accounts()
    log = open('tradelogs', 'w')
    buy(1.5, log, my_account[0], 'USD')
    sell(1.5, log, my_account[0], 'USD')
