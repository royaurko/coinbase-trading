import os
import hashlib
import hmac
import urllib.request
import urllib.error
import urllib.parse
import time
import json


# Set environmental variables with the names API_KEY and API_SECRET.


def make_request(url, body=None):
    opener = urllib.request.build_opener()
    nonce = int(time.time() * 1e6)
    message = str(nonce) + url + ('' if body is None else body)
    signature = hmac.new(str.encode(os.environ['API_SECRET']), str.encode(message), hashlib.sha256).hexdigest()
    headers = {'ACCESS_KEY': os.environ['API_KEY'],
               'ACCESS_SIGNATURE': signature,
               'ACCESS_NONCE': nonce,
               'Accept': 'application/json'}

    if body:
        headers.update({'Content-Type': 'application/json'})
        req = urllib.request.Request(url, data=str.encode(body), headers=headers)

    else:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        return response.read()
    try:
        return opener.open(req)
    except urllib.error.HTTPError as e:
        print(e)
        return e


def exchange_rate(currency='USD'):
    exchange_list = make_request('https://api.coinbase.com/v1/currencies/exchange_rates')
    exchange_list = json.loads(exchange_list.decode("utf-8"))
    return(float(exchange_list['btc_to_' + currency.lower()]))


def list_accounts():
    account_list = make_request('https://api.coinbase.com/v1/accounts')
    account_list = json.loads(account_list.decode("utf-8"))
    number = account_list['total_count']
    id_list = []
    for i in range(number):
        id_list.append(account_list['accounts'][i]['id'])
    return id_list


def query(account_id):
    balance = make_request('https://api.coinbase.com/v1/accounts/'+ account_id + '/balance')
    balance = json.loads(balance.decode("utf-8"))
    return(float(balance['amount']))


def buy(amount, log, account_id, currency='BTC', flag='n'):
    if flag == 'y':
        commit = 'true'
    else:
        commit = 'false'
    param = {
        'qty': amount,
        'commit': commit,
        'currency': currency,
        'account_id': account_id,
    }
    req = make_request('https://api.coinbase.com/v1/buys', body=json.dumps(param)).read()
    req = json.loads(req.decode("utf-8"))
    write_str = time.strftime("%m.%d.%y %H:%M ", time.localtime())
    write_str += 'Orders: '+ str(req['transfer']['description']) + ' , '
    write_str += 'Status: ' + str(req['transfer']['status']) + ' , '
    if req['success'] is False:
        write_str += 'Errors: ' + str(req['errors']) + ' , '
    write_str += 'Balance: ' + str(query(account_id)) + '\n'
    log.write(write_str.encode("utf-8"))


def sell(amount, log, account_id, currency='BTC', flag='n'):
    if flag == 'y':
        commit = 'true'
    else:
        commit = 'false'
    param = {
        'qty': amount,
        'commit': commit,
        'currency': currency,
        'account_id': account_id,
    }
    req = make_request('https://api.coinbase.com/v1/sells', body=json.dumps(param)).read()
    req = json.loads(req.decode("utf-8"))
    write_str = time.strftime("%m.%d.%y %H:%M ", time.localtime())
    write_str += 'Orders: ' + str(req['transfer']['description']) + ' , '
    write_str += 'Status: ' + str(req['transfer']['status']) + ' , '
    if req['success'] is False:
        write_str += 'Errors: ' + str(req['errors']) + ' , '
    write_str += 'Balance: ' + str(query(account_id)) + '\n'
    log.write(write_str.encode("utf-8"))


def status():
    status = make_request('https://api.coinbase.com/v1/orders')
    status = json.loads(status.decode("utf-8"))
    return status
