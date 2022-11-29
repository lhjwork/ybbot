import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests
import json
from .dbUse import order_save,select_uuids_market,tickers
from .orders import *
import pyupbit as up


server_url = 'https://api.upbit.com'

def method_headers(payload, secretkey):
     jwt_token = jwt.encode(payload, secretkey)
     authorize_token = 'Bearer {}'.format(jwt_token)
     headers = {"Authorization": authorize_token}
     return headers

def common_order(query,apikey,secretkey,avg_bid_price,user_id):

     query_string = urlencode(query).encode()

     m = hashlib.sha512()
     m.update(query_string)
     query_hash = m.hexdigest()
     payload = {
          'access_key': apikey,
          'nonce': str(uuid.uuid4()),
          'query_hash': query_hash,
          'query_hash_alg': 'SHA512',
     }
     # order_save(user_id,market,side,volume,price,uuid,ord_type):
     headers = method_headers(payload, secretkey)
     res = requests.post(server_url + "/v1/orders", params=query, headers=headers)
     
     saveData = res.json()

     split_step = 'split_one'
     panic_step = 'all_ask'

     try:
          # order_save(user_id,market,side,volume,price,uuid,ord_type,avg_bid_price,split_step,panic_step):
          order_save(str(user_id),saveData['market'],saveData['side'],saveData['volume'],saveData['price'],saveData['uuid'],saveData['ord_type'],avg_bid_price,split_step,panic_step)
     except Exception as ex:
          print('46 ',ex)
          return json.dumps({'errMsg':'fail_dbsave'}), 400,{'Content-Tpye':'application/json'}
     else:
          pass

     return saveData



def common_bid_order(query,apikey,secretkey,volume,split_step,panic_step,user_id):
     avg_bid_price = '0.0'
     query_string = urlencode(query).encode()


     m = hashlib.sha512()
     m.update(query_string)
     query_hash = m.hexdigest()
     payload = {
          'access_key': apikey,
          'nonce': str(uuid.uuid4()),
          'query_hash': query_hash,
          'query_hash_alg': 'SHA512',
     }
     # order_save(user_id,market,side,volume,price,uuid,ord_type):
     headers = method_headers(payload, secretkey)
     res = requests.post(server_url + "/v1/orders", params=query, headers=headers)
     
     saveData = res.json()
     print('common_bid_order saveData --->',saveData)


     try:
          # order_save(user_id,market,side,volume,price,uuid,ord_type,avg_bid_price):
          order_save(str(user_id),saveData['market'],saveData['side'],volume,saveData['price'],saveData['uuid'],saveData['ord_type'],avg_bid_price,split_step,panic_step)
     except Exception as ex:
          print('81 ',ex)
          return json.dumps({'errMsg':'fail_dbsave'}), 400,{'Content-Tpye':'application/json'}
     else:
          pass

     return saveData



