from __future__ import print_function
from glob import escape
from operator import le
import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests
import pyupbit
import datetime
import json
from .dbUse import * 
from flask import render_template,redirect


server_url = 'https://api.upbit.com'

def time_format(date_string):
     format_ = '%Y-%m-%dT%H:%M:%S+09:00'
     dt_strptime = datetime.datetime.strptime(date_string, format_)
     time = dt_strptime.strftime('%Y-%m-%d %H:%M:%S')
     return time

def total_askPrice(orderList):
     res_askPrice = float()
     last_askPrice = orderList[0]['price']
     last_askVolume  = orderList[0]['volume']
     last_resAskPirce = float(last_askPrice) * float(last_askVolume)
     for i in range(0, len(orderList)):
          price = orderList[i]['price']
          volume = orderList[i]['volume']
          ask_price = float(price) * float(volume)
          res_askPrice  = res_askPrice + ask_price

     return {'total_ask_price':res_askPrice,'last_ask_price':last_resAskPirce}


def order_check(access_key,secret_key):
     query = {
     'state': 'done',
     }
     query_string = urlencode(query)

     uuids = [
     # 'bd7c9b2c-9619-4dcd-9a38-373de4bdbd58',
     # '9a3c8430-d569-4e51-b263-d96f15bd0a93',
     #...
     ]
     uuids_query_string = '&'.join(["uuids[]={}".format(uuid) for uuid in uuids])

     query['uuids[]'] = uuids
     query_string = "{0}&{1}".format(query_string, uuids_query_string).encode()

     m = hashlib.sha512()
     m.update(query_string)
     query_hash = m.hexdigest()

     payload = {
     'access_key': access_key,
     'nonce': str(uuid.uuid4()),
     'query_hash': query_hash,
     'query_hash_alg': 'SHA512',
     }

     jwt_token = jwt.encode(payload, secret_key)
     authorize_token = 'Bearer {}'.format(jwt_token)
     headers = {"Authorization": authorize_token}

     res = requests.get(server_url + "/v1/orders", params=query, headers=headers)

     return res.json()

def current_qutation(market):
     
     market_dict = dict()
     url = f"https://api.upbit.com/v1/ticker?markets={market}"

     headers = {"Accept": "application/json"}

     response = requests.get(url, headers=headers)
     result = response.text
     try:
          result = json.loads(response.text)
     except Exception as ex:
          print('json.loads(response.text) err', ex)
          return redirect('/main')
     else:
          pass
     
     try: 
          cur_qutation = result[0]
          market_dict['market'] = cur_qutation['market']
          market_dict['trade_price'] = cur_qutation['trade_price']
     except Exception as ex:
          print('current_qutation error', ex)
     else:
          pass

     return market_dict


def all_accounts(access_key,secret_key):

     payload = {
     'access_key': access_key,
     'nonce': str(uuid.uuid4()),
     }

     jwt_token = jwt.encode(payload, secret_key)
     authorize_token = 'Bearer {}'.format(jwt_token)
     headers = {"Authorization": authorize_token}

     res = requests.get(server_url + "/v1/accounts", headers=headers)

     get_list = res.json()
     
     market_list = []
     for i in range(1,len(get_list)):
          market_dict = dict()
          currency =  get_list[i]['currency']
          avg_buy_price = get_list[i]['avg_buy_price']
          balance = get_list[i]['balance']
          user_money = float(avg_buy_price) * float(balance)
          unit_currency = get_list[i]['unit_currency']
          market_dict['market'] = f'{unit_currency}-{currency}'
          market_dict['all_buy'] = f'{user_money : .2f}'
          market_dict['all_volume'] = balance
          market_dict['avg_buy_price']= avg_buy_price
          market_list.append(market_dict)
     return market_list

def all_accounts_exclude_krw_krw(access_key,secret_key):
     

     payload = {
     'access_key': access_key,
     'nonce': str(uuid.uuid4()),
     }

     jwt_token = jwt.encode(payload, secret_key)
     authorize_token = 'Bearer {}'.format(jwt_token)
     headers = {"Authorization": authorize_token}

     res = requests.get(server_url + "/v1/accounts", headers=headers)

     get_list = res.json()
     print('get_list',get_list)
     
     if type(get_list) == type(dict()):
          # bid_datas = []
          return {'error':'wrong_key'}
     else :
          market_list = []
          markets = []
          for i in range(0,len(get_list)):
               market_dict = dict()
               currency =  get_list[i]['currency']
               avg_buy_price = get_list[i]['avg_buy_price']
               balance = get_list[i]['balance']
               user_money = float(avg_buy_price) * float(balance)
               unit_currency = get_list[i]['unit_currency']
               market = f'{unit_currency}-{currency}'
               market_dict['market'] = market
               market_dict['markets'] = markets.append(market)
               if market_dict['market'] != 'KRW-KRW':
                    market_dict['all_buy'] = f'{user_money : .2f}'
                    market_dict['all_volume'] = balance
                    market_dict['avg_buy_price']= avg_buy_price
                    market_list.append(market_dict)

     return market_list


def bid_history(access_key,secret_key):
     payload = {
     'access_key': access_key,
     'nonce': str(uuid.uuid4()),
     }

     jwt_token = jwt.encode(payload, secret_key)
     authorize_token = 'Bearer {}'.format(jwt_token)
     headers = {"Authorization": authorize_token}

     res = requests.get(server_url + "/v1/accounts", headers=headers)


     get_list = res.json()
     
     market_list = []
     for i in range(1,len(get_list)):
          market_dict = dict()
          currency =  get_list[i]['currency']
          avg_buy_price = float(get_list[i]['avg_buy_price'])
          balance = float(get_list[i]['balance'])
          unit_currency = get_list[i]['unit_currency']
          user_money = avg_buy_price * balance
          market = f'{unit_currency}-{currency}'

          current_trade = current_qutation(market)
          trade_price = float(current_trade['trade_price'])
          profit_rate = (trade_price * balance - user_money)/user_money
          profit_rate = f'{profit_rate * 100 : .2f}'
          profit_rate = float(profit_rate)

          market_dict['market'] = market
          market_dict['all_buy'] = f'{user_money : .2f}'
          market_dict['profit_rate'] = profit_rate
          
          market_list.append(market_dict)
     

     return market_list 




def current_bid_order_marketValue(user_id):
     #매수리스트 tanscations 에서 매수리스트 들고오기f
     bid_list_24hour = ask_list(user_id)
     temp_list = []
     
     
     
     for i in range(0,len(bid_list_24hour)):
          temp_dict = dict()
          market = bid_list_24hour[i]['market']
          try:
               cur_trade_list = current_qutation(market)
               # print('cur_trade_list---->',cur_trade_list)
          except:
               cur_trade_list == {}
          else:
               pass
               
          if len(cur_trade_list) == 0:
               pass
          else:
               cur_trade_price = cur_trade_list['trade_price']
               volume = bid_list_24hour[i]['volume']
               bid_price = bid_list_24hour[i]['price']
               # ==========================================
               cur_trade_price = float(cur_trade_price)
               volume = float(volume)
               bid_price = float(bid_price)
               rate_cur_bid = (cur_trade_price*volume - bid_price)/bid_price
               temp_dict['market'] = market
               temp_dict['bid_price'] = bid_price
               temp_dict['profit_rate'] = rate_cur_bid * 100
               temp_dict['work_time'] = bid_list_24hour[i]['work_time']
               temp_dict['auto_set'] = bid_list_24hour[i]['auto_set']
               temp_list.append(temp_dict)
          
     return temp_list

# 



def current_bid_order_marketValue_real(user_id):

     try:
          cur.execute("SELECT id, market, volume, bid_price, profit_rate, work_time, auto_set FROM orders WHERE (market,update_time) IN (select market, max(update_time) FROM orders where user_id = %s GROUP BY market) ORDER BY update_time DESC",(user_id,))
     except Exception as ex:
          print('current_bid_order_marketValue_real err',ex)
          balances_list = list()
          return balances_list
     else:
          temp_list = cur.fetchall()
          
          balances_list = list()
          for i in range(0,len(temp_list)):
               temp_dict = dict()
               temp_dict['id'] = temp_list[i][0]
               temp_dict['market'] = temp_list[i][1]
               temp_dict['volume'] = temp_list[i][2]
               temp_dict['bid_price'] = temp_list[i][3]
               temp_dict['profit_rate'] = temp_list[i][4]
               temp_dict['work_time'] = temp_list[i][5]
               temp_dict['auto_set'] = temp_list[i][6]
               balances_list.append(temp_dict)
               
          return balances_list



def completion_order(access_key,secret_key,user_id):

     # temp = ask_list(user_id)

     user_balances  = all_accounts_exclude_krw_krw(access_key,secret_key)
     # print('user_balances',user_balances)
     # print('user_balances',type(user_balances))
     if type(user_balances) == type(dict()):
          # bid_datas = []
          return {'error':'wrong_key'}
     else:
          completion_list = []
          
          
# user_balances 계좌 기준으로 market,all_buy,all_volume 호출 밑 셋업
          for i in range(0,len(user_balances)):
               temp_dict = dict()
               market = user_balances[i]['market']
               avg_buy_price =user_balances[i]['avg_buy_price']
               volume = user_balances[i]['all_volume']
               all_buy = user_balances[i]['all_buy']
               avg_buy_price = float(avg_buy_price)
               market_dict = current_qutation(market)
               try:
                    trade_price = float(market_dict['trade_price'])
                    dt = trade_price - avg_buy_price
                    profit_rate = dt / avg_buy_price
                    temp_dict['market'] = market
                    temp_dict['all_buy'] = all_buy
                    temp_dict['volume'] = volume
                    temp_dict['profit_rate'] = profit_rate * 100
                    completion_list.append(temp_dict)
               except Exception as ex:
                    print('completion_order',ex)
               else:
                    pass

     return completion_list

def completion_order_real(user_id):

     try:
          cur.execute("SELECT id, market, all_buy, volume, profit_rate, trade_time FROM balances WHERE (market,update_time) IN (select market,max(update_time) FROM balances where user_id = %s GROUP BY market) ORDER BY update_time DESC",(user_id,))
     except Exception as ex:
          print('completion_order_real err',ex)
          balances_list = list()
          return balances_list
     else:
          temp_list = cur.fetchall()
          
          balances_list = list()
          for i in range(0,len(temp_list)):
               temp_dict = dict()
               temp_dict['id'] = temp_list[i][0]
               temp_dict['market'] = temp_list[i][1]
               temp_dict['all_buy'] = temp_list[i][2]
               temp_dict['volume'] = temp_list[i][3]
               temp_dict['profit_rate'] = temp_list[i][4]
               temp_dict['trade_time'] = temp_list[i][5]
               balances_list.append(temp_dict)
               
          return balances_list
          
# # user_balances 계좌 기준으로 market,all_buy,all_volume 호출 밑 셋업
#           for i in range(0,len(user_balances)):
#                temp_dict = dict()
#                market = user_balances[i]['market']
#                avg_buy_price =user_balances[i]['avg_buy_price']
#                volume = user_balances[i]['all_volume']
#                all_buy = user_balances[i]['all_buy']
#                avg_buy_price = float(avg_buy_price)
#                market_dict = current_qutation(market)
#                try:
#                     trade_price = float(market_dict['trade_price'])
#                     dt = trade_price - avg_buy_price
#                     profit_rate = dt / avg_buy_price
#                     temp_dict['market'] = market
#                     temp_dict['all_buy'] = all_buy
#                     temp_dict['volume'] = volume
#                     temp_dict['profit_rate'] = profit_rate * 100
#                     completion_list.append(temp_dict)
#                except Exception as ex:
#                     print('completion_order',ex)
#                else:
#                     pass

#      return completion_list


def week_profit_datas(user_id):
     try:
          cur.execute('SELECT trade_count,sum_profit_rate,update_time FROM week_profit WHERE user_id =%s ORDER BY update_time desc limit 7',(user_id,))
     except Exception as ex:
          print('week_profit_datas',ex)
     else:
          temp = cur.fetchall()

          profit_rate_list = []
          week_dataList = []
          if temp == []:
     
               temp_dict = dict()
               temp_dict['trade_count'] = 0
               temp_dict['profit_rate'] = 0
               temp_dict['update_time'] = ''
               week_dataList.append(temp_dict)
               max_profit_rate = 0
          else:

               for i in range(0,len(temp)):
                    temp_dict = dict()
                    temp_dict['trade_count'] = temp[i][0]
                    profit_rate = temp[i][1]
                    profit_rate = float(profit_rate)*100
                    temp_dict['profit_rate'] = profit_rate
                    update_time = temp[i][2]
                    update_time = update_time.strftime("%Y/%m/%d")
                    temp_dict['update_time'] = update_time[2:]
                    week_dataList.append(temp_dict)
                    profit_rate_list.append(abs(profit_rate))
                    max_profit_rate = max(profit_rate_list)
     return {'week_data_list':week_dataList,'max_profit_rate':max_profit_rate}, 200


          # user_balances 계좌 기준으로 market,all_buy,all_volume 호출 밑 셋업
          # lask_ask_dict 담긴 데이터와 user_balance데이터를 비교
          
               

          # 코인명, 수익금, 수익률, 마지막 매도 금액,마지막 volume을 market 별로 던져 주기

          
                    



