from kiteconnect import KiteConnect

apiKey = 'dummy text'
apiSecret = 'dummy text'

requestToken = 'dummy text'

accessToken = 'dummy text'

kite = KiteConnect(api_key = apiKey)


# data = kite.generate_session(requestToken,api_secret=apiSecret)
# print(data)


kite.set_access_token(accessToken)

# print(kite.orders)

"""
url to generate request token:
https://kite.trade/connect/login?api_key=dummy text
"""




