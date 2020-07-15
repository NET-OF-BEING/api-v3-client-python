#!/usr/bin/python3
import base64
import yaml
import pprint
import hashlib
import hmac
import time
import json
import config
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

base_url = 'https://api.btcmarkets.net'


def makeHttpCall(method, apiKey, privateKey, path, queryString, data=None):
    if data is not None:
        data = json.dumps(data)

    headers = buildHeaders(method, apiKey, privateKey, path, data)
    fullPath = ''
    if queryString is None:
        fullPath = path
    else:
        fullPath = path + '?' + queryString

    try:
        http_request = Request(base_url + fullPath, data, headers, method = method)

        if method == 'POST' or method == 'PUT':
            response = urlopen(http_request, data = bytes(data, encoding="utf-8"))
        else:
            response = urlopen(http_request)

        return json.loads(str(response.read(), "utf-8"))
    except URLError as e:
        errObject = json.loads(e.read())
        if hasattr(e, 'code'):
            errObject['statusCode'] = e.code

        return errObject


def buildHeaders(method, apiKey, privateKey, path, data):
    now = str(int(time.time() * 1000))
    message = method + path + now
    if data is not None:
        message += data

    signature = signMessage(privateKey, message)

    headers = {
        "Accept": "application/json",
        "Accept-Charset": "UTF-8",
        "Content-Type": "application/json",
        "BM-AUTH-APIKEY": apiKey,
        "BM-AUTH-TIMESTAMP": now,
        "BM-AUTH-SIGNATURE": signature
    }

    return headers


def signMessage(privateKey, message):
    presignature = base64.b64encode(hmac.new(
        privateKey, message.encode('utf-8'), digestmod=hashlib.sha512).digest())
    signature = presignature.decode('utf8')

    return signature


class BTCMarkets:

    def __init__(self, apiKey, privateKey):
        self.apiKey = apiKey
        self.privateKey = base64.b64decode(privateKey)

    def get_orders(self):
        print("ORDERS")
        print('----------------------------------------------')
        return makeHttpCall('GET', self.apiKey, self.privateKey, '/v3/orders', 'status=all')
        print('----------------------------------------------\n\n')

    def open_all_orders(self):
        print("OPEN ALL ORDERS")
        print('----------------------------------------------\n\n')
        instrument = input("Enter instrument: ")
        currency  = input("Enter currency: ")
        return makeHttpCall('GET', self.apiKey, self.privateKey, '/v2/order/open[/{instrument}/{currency}', 'status=all')
    
    def get_order_book(self):
        marketId  = input("Enter Market ID: ")
        print("MARKET ID")
        print('----------------------------------------------')
        return makeHttpCall('GET', self.apiKey, self.privateKey, '/v3/markets/{marketId}/orderbook', marketId,'status=none')
        print('----------------------------------------------\n\n')
    
    def get_order_history(self):
        print("ORDER HISTORY")
        print('----------------------------------------------')
        return makeHttpCall('GET', self.apiKey, self.privateKey, '/v3/orders', 'status=none')
        print('----------------------------------------------\n\n')
    
    
    def get_order_details(self):
        print("ORDER DETAILS")
        print('----------------------------------------------')
        return makeHttpCall('POST', self.apiKey, self.privateKey, '/order/detail', 'status=all')
        print('----------------------------------------------\n\n')
    
    def get_trade_history(self):
        print("TRADE HISTORY")
        print('----------------------------------------------')
        return makeHttpCall('GET', self.apiKey, self.privateKey, '/v3/trade','status=all')
        print('----------------------------------------------\n\n')
        
    #def get_trade_history(self):
        #instrument = input("Enter instrument: ")
        #currency  = input("Enter currency: ")
        #limit = input("Enter limit: ")
        #since  = input("Enter since: ")
        #print("TRADE HISTORY")
        #print('----------------------------------------------')
        #return makeHttpCall('GET', self.apiKey, self.privateKey, '/v2/order/trade/history/{instrument}/{currency}/limit={limit}&since={since}','status=all')
        #print('----------------------------------------------\n\n')
    
    def account_balance(self):
        print("ACCOUNT BALANCE")
        print('----------------------------------------------\n\n')
        return makeHttpCall('GET', self.apiKey, self.privateKey, '/v3/accounts/me/balances', 'status=all')

    def get_open_orders(self):
        print("OPEN ORDERS")
        print('----------------------------------------------\n\n')
        return makeHttpCall('POST', self.apiKey, self.privateKey, '/v2/order/open', 'status=all')
    
    def get_deposits(self):
        print("LIST DEPOSITS")
        print('----------------------------------------------\n\n')
        return makeHttpCall('GET', self.apiKey, self.privateKey, '/v3/deposits', 'status=all')
    
    def deposits_withdrawals(self):
        before = input("Before: ")
        after = input("After: ")
        limit = input("Limit: ")
        print("DEPOSITS / WITHDRAWALS")
        print('----------------------------------------------\n\n')
        return makeHttpCall('GET', self.apiKey, self.privateKey, '/v3/transfers/', '?before=before&after=after&limit=limit', 'status=all')
    
    def get_deposit_address(self):
        assetName = input("Enter asset: ")
        print("COIN ADDRESS")
        print('----------------------------------------------\n\n')
        return makeHttpCall('GET', self.apiKey, self.privateKey, '/v3/addresses',assetName, 'status=all')

    def withdraw(self):
        print("ACCOUNT BALANCE")
        print('----------------------------------------------\n\n')
        return makeHttpCall('GET', self.apiKey, self.privateKey, '/v3/accounts/me/balances', 'status=all')
    
    def place_new_order(self):
        marketID = input("Enter Market ID: ")
        price= input("Enter Price: ")
        amount = input("Enter Amount: ")
        orderType= input("Enter Order Type: ")
        orderSide= input("Enter Order Side: ")

        model = {
            'marketID': marketID,
            'price': price,
            'amount': amount,
            'type': orderType,
            'side': orderSide
        }
        return makeHttpCall('POST', self.apiKey, self.privateKey, '/v3/orders', None, model)

    def replace_order(self):
        orderID = input("Enter Order ID: ")
        price= input("Enter Price: ")
        amount = input("Enter Amount: ")
        clientOrderId = input("Enter Amount: ")
        model = {
            'price': price,
            'amount': amount,
            'clientOrderId': clientOrderId,
        }
        return makeHttpCall('PUT', self.apiKey, self.privateKey, '/v3/orders/',id,model)

    def cancel_order_id(self):
        orderID = input("Enter OrderID: ")
        print("CANCEL ORDER BY ID")
        print('----------------------------------------------\n\n')
        return makeHttpCall('DELETE', self.apiKey, self.privateKey, '/v3/orders/',orderID)
    
    def server_time(self):
        return makeHttpCall('GET', self.apiKey, self.privateKey, '/v3/time','status=none')
    
    def get_asset(self):
        return makeHttpCall('GET', self.apiKey, self.privateKey, '/v3/assets','status=none')
    
    def cancel_order_market(self):
        marketID = input("MarketID: ")
        print("CANCEL ORDER BY MARKET")
        print('----------------------------------------------\n\n')
        return makeHttpCall('DELETE', self.apiKey, self.privateKey, '/v3/orders',marketID)
    
    def withdrawal_fees(self):
        print("WITHDRAWAL FEES")
        print('----------------------------------------------\n\n')
        return makeHttpCall('GET', self.apiKey, self.privateKey, '/v3/withdrawal-fees', 'status=none')
    
    def my_transactions(self):
        coin = input("Enter Coin: ")
        return makeHttpCall('GET', self.apiKey, self.privateKey, '/v3/accounts/me/transactions/',coin)



if __name__ == "__main__":

    api_key = config.api_key
    print(api_key)
    private_key = config.private_key
    client = BTCMarkets(api_key, private_key)
    menuchoices = {'1':client.account_balance, '2':client.get_order_details,'3':client.get_order_book,'4':client.get_order_history,'5':client.get_trade_history,'6':client.open_all_orders,'7':client.get_open_orders,'8':client.get_orders,'9':client.get_deposit_address,'t':client.my_transactions,'a':client.server_time,'w':client.withdrawal_fees,'c':client.get_asset,'x':client.cancel_order_market,'l':client.cancel_order_id,'v':client.get_deposits,'g':client.place_new_order,'r':client.replace_order,'y':client.deposits_withdrawals}

    def menu(self):
        print('''
   ______        _________    ________          _____ ______       ________      ________      ___  __        _______       _________    ________      
  |\   __  \    |\___   ___\ |\   ____\        |\   _ \  _   \    |\   __  \    |\   __  \    |\  \|\  \     |\  ___ \     |\___   ___\ |\   ____\     
  \ \  \|\ /_   \|___ \  \_| \ \  \___|        \ \  \\\__\ \  \   \ \  \|\  \   \ \  \|\  \   \ \  \/  /|_   \ \   __/|    \|___ \  \_| \ \  \___|_    
   \ \   __  \       \ \  \   \ \  \            \ \  \\|__| \  \   \ \   __  \   \ \   _  _\   \ \   ___  \   \ \  \_|/__       \ \  \   \ \_____  \   
    \ \  \|\  \       \ \  \   \ \  \____        \ \  \    \ \  \   \ \  \ \  \   \ \  \\  \|   \ \  \\ \  \   \ \  \_|\ \       \ \  \   \|____|\  \  
     \ \_______\       \ \__\   \ \_______\       \ \__\    \ \__\   \ \__\ \__\   \ \__\\ _\    \ \__\\ \__\   \ \_______\       \ \__\    ____\_\  \ 
      \|_______|        \|__|    \|_______|        \|__|     \|__|    \|__|\|__|    \|__|\|__|    \|__| \|__|    \|_______|        \|__|   |\_________\
                                                                                                                                           \|_________|
        ''')
        print("---------------------------------")
        print("Select an option:")
        print("---------------------------------\n")
        print("1. Account Balance ")
        print("2. Order Details")
        print("3. Get Order Book")
        print("4. Order History")
        print("5. Trade History")
        print("6. Open All Orders")
        print("7. Open Orders")
        print("8. Orders")
        print("9. Deposit Address")
        print("v, List Deposits")
        print("t. My Transactions")
        print("a. Server Time")
        print("x. Cancel Order by Market ID")
        print("l. Cancel Order by Order ID")
        print("0. Sell quote")
        print("o. My Orders")
        print("h. Orders History")
        print("w. Withdrawal Fees")
        print("y. List Deposits/Withdrawals")
        print("c. Assets")
        print("r. Replace an Order")
        print("g. Place Buy Order")
        print("p. Place Sell Order")
        print("q. Quit\n\n")
        print("----------------------------------\n")
    
        ret = menuchoices[input("Option: ")]()
        pprint.pprint(ret)
        #if ret is None:
        #    print("Please enter a valid menu choice!")
        #menuchoices['q']()

menu(client)
#print(order)
#print(yaml.dump(order, default_flow_style="True", default_style=""))
#pprint.pprint(client.account_balance())
#print(yaml.dump(client.place_new_order()))
#print(yaml.dump(client.cancel_order()))
#pprint.pprint(yaml.dump(client.get_trade_history()))
#pprint.pprint(yaml.dump(client.get_order_book()))
