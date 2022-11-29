# from quotation import quo_orderbook
import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests
import json
from .orderCommon import common_bid_order,common_order
from .dbUse import order_save,select_uuids_market,select_orderMarket
import pyupbit


# bid : 매수 / ask:매도
# 지정가 매수/매도
# re
def bid_order(apikey,secretkey,price,ticker,split_step,panic_step,user_id):
     # 호가 
     # res = quo_orderbook('KRW-BTC')
     cur_price = pyupbit.get_current_price(ticker)

     cur_price = float(cur_price)
     
     price = float(price)
     volume = price * (1/cur_price)
     query ={
          'market':ticker,
          'side':'bid',
          'price':price,
          'ord_type':'price',
          # 'ord_type':'market',
     }
     

     # common_bid_order(query,apikey,secretkey,volume,user_id)
     res = common_bid_order(query,apikey,secretkey,volume,split_step,panic_step,user_id)
     

     return res

# bid_order(apikey,secretkey,volume,price,tickers):
def ask_order(volume,trade_price,accessKey,ticker,secretkey,avg_bid_price,user_id):
     # 호가 

     volume = float(volume)
     trade_price = float(trade_price)
     

     query = dict()
     query ={
          'market':ticker,
          'side':'ask',
          'volume':volume,
          'price':trade_price,
          # 'ord_type':'limit',
          'ord_type':'market',
     }
     res = common_order(query,accessKey,secretkey,avg_bid_price,user_id)
     return res



def cur_qutation(market):
     url = f"https://api.upbit.com/v1/ticker?markets={market}"

     headers = {"Accept": "application/json"}

     response = requests.get(url, headers=headers)

     cur_trade_price = response.json()[0]['trade_price']
     return cur_trade_price

