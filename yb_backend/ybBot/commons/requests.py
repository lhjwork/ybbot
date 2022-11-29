import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests
import json
import time
# from .dbConnFetch import *

# conn = dbConn_no_cur()
# cur = conn.cursor()


headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}


def api_bidPass(price,tickers,accessKey,secretKey,split_step,panic_step,invest_type,user_id):

     temp_data = dict()
     temp_data = {
          'price':price,
          'tickers':tickers,
          'accessKey':accessKey,
          'secretKey':secretKey,
          'split_step':split_step,
          'panic_step':panic_step,
          'auto_set':invest_type,
          'user_id':user_id
     }
     try: 
          response = requests.post(f'http://127.0.0.1:5000/bidpass', data = json.dumps(temp_data),headers=headers)
          time.sleep(1)
     except Exception as ex:
          return {'errMsg',ex}
     else:
          pass
     return response 




# 현재가 조회
def current_trade_price(ticker):
     
     url = f"https://api.upbit.com/v1/ticker?markets={ticker}"

     headers = {"Accept": "application/json"}

     response = requests.get(url, headers=headers)
     data = response.json()[0]
     return data['trade_price']

def api_askPass(trade_price,volume,ticker,accessKey,secretKey,avg_bid_price,invest_type,user_id):
     temp_data = dict()
     temp_data = {
          'volume':volume,
          'trade_price':trade_price,
          'ticker':ticker,
          'accessKey':accessKey,
          'secretKey':secretKey,
          'avg_bid_price':avg_bid_price,
          'auto_set':invest_type,
          'user_id':user_id
     }
     try: 
          response = requests.post(f'http://127.0.0.1:5000/askpass', data = json.dumps(temp_data), headers=headers)
     except Exception as ex:
          return {'errMsg',ex}
     else:
          pass
     return response 
