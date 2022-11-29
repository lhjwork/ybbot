from operator import le
import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests
import pyupbit
import datetime
from .dbUse import * 


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
     result = response.json()[0]
     market_dict['market'] = result['market']
     market_dict['trade_price'] = result['trade_price']
     
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




def current_bid_order_marketValue(access_key,secret_key,user_id):
     #매수리스트 tanscations 에서 매수리스트 들고오기f
     user_id = 1
     bid_list_24hour = ask_list(user_id)
     temp_list = []
     for i in range(0,len(bid_list_24hour)):
          temp_dict = dict()
          market = bid_list_24hour[i]['market']
          cur_trade_list =current_qutation(market)
          # ========================= =================
          cur_trade_price = cur_trade_list['trade_price']
          # volume = bid_list_24hour[i]['volume']
          bid_price = bid_list_24hour[i]['price']
          # ==========================================
          cur_trade_price = float(cur_trade_price)
          # volume = float(volume)
          bid_price = float(bid_price)
          rate_cur_bid = (cur_trade_price - bid_price)/bid_price
          temp_dict['market'] = market
          temp_dict['bid_price'] = bid_price
          temp_dict['profit_rate'] = rate_cur_bid
          temp_dict['work_time'] = bid_list_24hour[i]['work_time']
          temp_dict['auto_set'] = bid_list_24hour[i]['auto_set']
          temp_list.append(temp_dict)
          
     return temp_list

# 



def completion_order(access_key,secret_key,user_id):


     user_balances  = all_accounts(access_key,secret_key)
     # user_balances = bid_history(access_key,secret_key)

     completion_list = []
# user_balances 계좌 기준으로 market,all_buy,all_volume 호출 밑 셋업
     for i in range(0,len(user_balances)):
          market = user_balances[i]['market']
          # print('market~~~~~~>',market)
          avg_buy_price =user_balances[i]['avg_buy_price']
          avg_buy_price = float(avg_buy_price)
          upbit = pyupbit.Upbit(access_key,secret_key)
          orders = upbit.get_current_price(market)
          # print('orders'*20,orders)
          # 전체 주문 호출 후 ask(매도) 부분 만 데이터 정제
          for k in range(0,len(orders)):
               # while orders[k]['side'] == 'bid':
               if orders[k]['side'] == 'ask':
               
                    last_ask_dict = dict()
                    last_ask_dict['market'] = orders[k]['market']
                    last_ask_dict['side'] = orders[k]['side']
                    last_ask_dict['price'] = orders[k]['price']
                    last_ask_dict['created_at'] = orders[k]['created_at']
                    last_ask_dict['volume'] = orders[k]['volume']
                    # break
               else:
          

          # print(f'last_ask_dict(market) ==user_balances[{i}][market]',last_ask_dict['market'], user_balances[i]['market'])
          # if last_ask_dict['market'] == user_balances[i]['market']:
                    last_temp_dict = dict()
                    market = last_ask_dict['market']
                    last_ask_price = last_ask_dict['price']
                    last_ask_volume = last_ask_dict['volume']
                    last_ask_time = time_format(last_ask_dict['created_at'])
                    last_ask_price = float(last_ask_price) 
                    last_ask_volume = float(last_ask_volume)
               
                    trnscPrice = last_ask_price * last_ask_volume
                    before_trnscPrice = float(user_balances[i]['all_buy']) + trnscPrice
                    current_value = avg_buy_price * last_ask_volume
                    profit_rate = (current_value - before_trnscPrice) / before_trnscPrice
                    # 코인명, 거래금액,수익률, 마지막 volume을 market 별로 던져 주기
                    # ['market':market,'trnscPrice':trnscPrice,'profit_rate':profit_rate,'last_ask_volume ':last_ask_volume,'last_ask_time':last_ask_time]
                    last_temp_dict['market'] = market
                    last_temp_dict['trnscPrice'] = trnscPrice
                    last_temp_dict['profit_rate'] = profit_rate
                    last_temp_dict['last_ask_volume'] = last_ask_volume
                    last_temp_dict['last_ask_time'] = last_ask_time
                    completion_list.append(last_temp_dict)
                    
          # 계산:  거래전가격 - 평균 매도가격 * last_ask_volume / 거래전 가격전체
     return completion_list


          

def week_profit_datas(user_id):
     try:
          cur.execute('SELECT trade_count,sum_profit_rate,update_time FROM week_profit WHERE user_id =%s ORDER BY update_time desc limit 7',(user_id,))
     except Exception as ex:
          print('week_profit_datas',ex)
     else:
          temp = cur.fetchall()
          week_dataList = []
          for i in range(0,len(temp)):
               temp_dict = dict()
               temp_dict['trade_count'] = temp[i][0]
               profit_rate = temp[i][1]
               temp_dict['profit_rate'] = float(profit_rate)*100 
               update_time = temp[i][2]
               update_time = update_time.strftime("%Y/%m/%d")
               temp_dict['update_time'] = update_time[2:]
               week_dataList.append(temp_dict)
     return week_dataList, 200



          # user_balances 계좌 기준으로 market,all_buy,all_volume 호출 밑 셋업
          # lask_ask_dict 담긴 데이터와 user_balance데이터를 비교
          
               

          # 코인명, 수익금, 수익률, 마지막 매도 금액,마지막 volume을 market 별로 던져 주기

          
                    



