import os
import hashlib
import hmac
import urllib.request
import urllib.error
import urllib.parse
import time
import json

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

    # If we are passing data, a POST request is made. Note that content_type is specified as json.
    if body:
        headers.update({'Content-Type': 'application/json'})
        req = urllib.request.Request(url, data=str.encode(body), headers=headers)

    # If body is nil, a GET request is made.
    else:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        return response.read()
    try:
        return opener.open(req)
    except urllib.error.HTTPError as e:
        print(e)
        return e

# Example of a GET request, where body is nil.


def query(id=None):
    balance = make_request('https://api.coinbase.com/v1/account/balance')
    balance = balance.decode("utf-8")
    print(balance)


def buy(amount):
    param = {
        'qty': .01,
        'commit': 'false',
    }
    req = make_request('https://api.coinbase.com/v1/buys', body=json.dumps(param)).read()
    req = req.decode("utf-8")
    print(req)


def sell(amount):
    param = {
        'qty': .01,
        'commit': 'false',
    }
    req = make_request('https://api.coinbase.com/v1/sells', body=json.dumps(param)).read()
    req = req.decode("utf-8")
    print(req)



if __name__ == '__main__':
    query()
    sell(0.01)
