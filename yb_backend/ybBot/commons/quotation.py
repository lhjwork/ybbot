import requests
import json

# 시세는 소켓으로 해야함

# '호가 정보'는 시장이 어떤 종목을 얼마에 얼마나 많이 매매하려하고 있는지를 알려주는 정보
url = "https://api.upbit.com/v1/orderbook"


def quo_orderbook(ticker):
    
     # ticker = 'KRW-BTC'
     headers = {"Accept": "application/json"}
     response = requests.get("https://api.upbit.com/v1/orderbook?markets={}".format(ticker), headers=headers)
     # response.text : text 속성을 통해 UTF-8로 인코딩된 문자열을 받을 수 있다.
     
     return response.text


#전일 종가 대비
def quo_day_orderbook(ticker):
     
     url = f"https://api.upbit.com/v1/candles/days?market={ticker}&count=1&convertingPriceUnit=KRW"

     headers = {"Accept": "application/json"}

     response = requests.get(url, headers=headers)
     result = json.loads(response.text)

     return result



# def day_quotation(ticker):
     
#      url = f"https://api.upbit.com/v1/candles/days?market={ticker}&count=1&convertingPriceUnit=KRW"

#      headers = {"Accept": "application/json"}

#      response = requests.get(url, headers=headers)

     
#      result = json.loads(response.text)
#      print('day_quotation',result)

#      return result