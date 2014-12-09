import os
import hashlib
import hmac
import urllib.request
import urllib.error
import urllib.parse
import time
import json
import ast


#Before implementation, set environmental variables with the names API_KEY and API_SECRET.


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



def query(id=None):
    balance = make_request('https://api.coinbase.com/v1/account/balance')
    balance = json.loads(balance.decode("utf-8"))
    print(balance['amount'], ' BTC')


def buy(amount, currency='BTC'):
    param = {
        'qty': amount,
        'commit': 'false',
        'currency': currency,
    }
    req = make_request('https://api.coinbase.com/v1/buys', body=json.dumps(param)).read()
    req = json.loads(req.decode("utf-8"))
    print('Order: ', req['transfer']['description'])
    print('Status: ', req['transfer']['status'])
    if req['success'] == False:
        print('Error: ', req['errors'])

def sell(amount, currency='BTC'):
    param = {
        'qty': amount,
        'commit': 'false',
        'currency': currency,
    }
    req = make_request('https://api.coinbase.com/v1/sells', body=json.dumps(param)).read()
    req = json.loads(req.decode("utf-8"))
    print('Order: ', req['transfer']['description'])
    print('Status: ', req['transfer']['status'])
    if req['success'] == False:
        print('Errors: ', req['errors'])

def status():
    status = make_request('https://api.coinbase.com/v1/orders')
    status = ast.literal_eval(status.decode("utf-8"))
    print(status)


if __name__ == '__main__':
    query()
    #status()
    buy(1.5, currency='USD')
    sell(1.5, currency='USD')
