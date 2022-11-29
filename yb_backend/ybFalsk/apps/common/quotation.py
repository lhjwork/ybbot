from urllib.parse import urlencode

import requests

# 시세는 소켓으로 해야함

# '호가 정보'는 시장이 어떤 종목을 얼마에 얼마나 많이 매매하려하고 있는지를 알려주는 정보
url = "https://api.upbit.com/v1/orderbook"


def quo_orderbook(ticker):

     # ticker = 'KRW-BTC'
     headers = {"Accept": "application/json"}
     response = requests.get("https://api.upbit.com/v1/orderbook?markets={}".format(ticker), headers=headers)
     # response.text : text 속성을 통해 UTF-8로 인코딩된 문자열을 받을 수 있다.
     return response.text


