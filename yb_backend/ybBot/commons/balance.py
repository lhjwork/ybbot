
from curses import resetty
from re import A
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import pyupbit
import datetime
from .constant import * 
import requests
import json
from .dbConnFetch import *
import time

conn == dbConn_no_cur()
cur == conn.cursor()





def time_format(date_string):
     format_ = '%Y-%m-%dT%H:%M:%S+09:00'
     dt_strptime = datetime.datetime.strptime(date_string, format_)
     time = dt_strptime.strftime('%Y-%m-%d %H:%M:%S')
     return time

def users_left_balance(access_key,secret_key):

     payload = {
     'access_key': access_key,
     'nonce': str(uuid.uuid4()),
     }

     jwt_token = jwt.encode(payload, secret_key)
     authorize_token = 'Bearer {}'.format(jwt_token)
     headers = {"Authorization": authorize_token}

     res = requests.get(server_url + "/v1/accounts", headers=headers)
     # print('left_balance ======>',res.json()[0])
     left_balance = res.json()[0]


     return left_balance 




def all_accounts(access_key,secret_key,user_id):
     # print('user_id',user_id)
     
     payload = {
     'access_key': access_key,
     'nonce': str(uuid.uuid4()),
     }

     jwt_token = jwt.encode(payload, secret_key)
     authorize_token = 'Bearer {}'.format(jwt_token)
     headers = {"Authorization": authorize_token}

     res = requests.get(server_url + "/v1/accounts", headers=headers)
     # print('res',res)
     get_list = res.json()
     # print('get_list',get_list)

     if type(get_list) == type(dict()):
          return {'error':'failed'}
     else:
          seed_money = get_list[0]['balance']

     market_list = []
     for i in range(0,len(get_list)):

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
          market_dict['seed_money'] = seed_money
                    
          market_list.append(market_dict)


     return market_list

def seed_status(access_key,secret_key):
     payload = {
     'access_key': access_key,
     'nonce': str(uuid.uuid4()),
     }

     jwt_token = jwt.encode(payload, secret_key)
     authorize_token = 'Bearer {}'.format(jwt_token)
     headers = {"Authorization": authorize_token}

     res = requests.get(server_url + "/v1/accounts", headers=headers)
     get_list = res.json()

     if type(get_list) == type(dict()):
     
          return {'error':'failed'}
     else:
          seed_money = get_list[0]['balance']

     market_list = []
     for i in range(0,len(get_list)):
          market_dict = dict()
          currency =  get_list[i]['currency']
          if currency == 'KRW':
               balance = get_list[i]['balance']
               unit_currency = get_list[i]['unit_currency']
               market_name = f'{unit_currency}-{currency}'
               market_dict['market'] = market_name
               market_dict['seed_money'] = balance
               market_list.append(market_dict)
          
     return market_list



def cur_qutation(market):
     market_dict = dict()
     url = f"https://api.upbit.com/v1/candles/minutes/1?market={market}&count=1"

     headers = {"Accept": "application/json"}

     response = requests.get(url, headers=headers)
     
     try:
          result = json.loads(response.text)
          market_dict['market'] = result[0]['market']
          market_dict['trade_price'] = result[0]['trade_price']
     except:
          pass
     else:
          pass

     return market_dict



def bid_history(access_key,secret_key):

     market_list = []
     try:
          payload = {
          'access_key': access_key,
          'nonce': str(uuid.uuid4()),
          }
          jwt_token = jwt.encode(payload,secret_key)
          authorize_token = 'Bearer {}'.format(jwt_token)
          headers = {"Authorization": authorize_token}
          res = requests.get(server_url + "/v1/accounts", headers=headers)
          get_list = res.json()
          print('get_list',get_list)
     except Exception as ex:
          print(ex)
     else:
          
          for i in range(1,len(get_list)):
               market_dict = dict()
               currency =  get_list[i]['currency']
               avg_buy_price = float(get_list[i]['avg_buy_price'])
               balance = float(get_list[i]['balance'])
               unit_currency = get_list[i]['unit_currency']
               volume = get_list[i]['balance']
          
               user_money = avg_buy_price * balance
               market = f'{unit_currency}-{currency}'

               if market != 'KRW-KRW':
                    current_trade = cur_qutation(market)

                    if len(current_trade) != 0:
                         trade_price = float(current_trade['trade_price'])
                         try:
                              profit_rate = (trade_price * balance - user_money)/user_money
                              profit_rate = f'{profit_rate * 100 : .2f}'
                              profit_rate = float(profit_rate)
                         except:
                              profit_rate = 0.0
                         else:
                              pass

                         market_dict['market'] = market
                         market_dict['all_buy'] = f'{user_money : .2f}'
                         market_dict['profit_rate'] = profit_rate
                         market_dict['volume'] = volume
                         market_dict['avg_bid_price'] = avg_buy_price
                         market_dict['result'] = 'success'
                         market_list.append(market_dict)
     
     
               return market_list 

# 

def auto_ask_entry(profit):

     for ask_entry_count in range(0,59):
     
          ask_entry = ask_entry_count + 3   
          # swing_entry = 1.5 + 0.8*i

          if ask_entry <= profit :
               return ask_entry_count

     
     
def swing_entry(ask_entry_count,profit_rate,market):
     swing_entry = 1.5 + 0.8*ask_entry_count
     
     if profit_rate <= swing_entry:
          return {'result':'success'}
     else:
     
          return {'result':f'{market} ask 대기'}
     



def user_left_voucher(user_id):
     # print('user_id',user_id)
     try:
          cur.execute("SELECT SUM(voucher),SUM(used_voucher) from voucher where user_id = %s AND NOW() <= finish_time",(user_id,))
     except Exception as ex:
          print('user_last_voucher err',ex)
     else:
          voucher_infos = cur.fetchone()
          # print('balacne',voucher_infos)
          left_voucher = voucher_infos[0] - voucher_infos[1]
     return left_voucher

def decrease_special_invest_save(market,trade_price,change_rate,type):
     try:
          cur.execute("INSERT INTO rate(market,trade_price,change_rate,type) VALUES(%s,%s,%s,%s)",(market,trade_price,change_rate,type))
     except Exception as ex:
          conn.rollback()
     else:
          conn.commit()
     return {'result':'success'}

def all_accounts_exclude_krw_krw(access_key,secret_key):
     time.sleep(1)
     payload = {
     'access_key': access_key,
     'nonce': str(uuid.uuid4()),
     }

     jwt_token = jwt.encode(payload, secret_key)
     authorize_token = 'Bearer {}'.format(jwt_token)
     headers = {"Authorization": authorize_token}

     res = requests.get(server_url + "/v1/accounts", headers=headers)

     try:
          get_list = res.json()
     except Exception as ex:
          print('get_list err',ex)
     else:
          pass

     if type(get_list) == type(dict()):
          # bid_datas = []
          return {'error':'wrong_key'}
     else :
          market_list = []
          for i in range(0,len(get_list)):
               market_dict = dict()
               currency =  get_list[i]['currency']
               avg_buy_price = get_list[i]['avg_buy_price']
               balance = get_list[i]['balance']
               user_money = float(avg_buy_price) * float(balance)
               unit_currency = get_list[i]['unit_currency']
               market_dict['market'] = f'{unit_currency}-{currency}'
               
               if market_dict['market'] != 'KRW-KRW':
                    market_dict['all_buy'] = f'{user_money : .2f}'
                    market_dict['all_volume'] = balance
                    market_dict['avg_buy_price']= avg_buy_price
                    market_list.append(market_dict)

     return market_list


def current_qutation(market):
     
     market_dict = dict()
     try:
          url = f"https://api.upbit.com/v1/ticker?markets={market}"

          headers = {"Accept": "application/json"}

          response = requests.get(url, headers=headers)
          result = response.text
          result = json.loads(response.text)
     except Exception as ex:
          pass
     else:
          pass
     if type(result) != dict:
          try: 
               cur_qutation = result[0]
               market_dict['market'] = cur_qutation['market']
               market_dict['trade_price'] = cur_qutation['trade_price']
          except Exception as ex:
               pass
          else:
               pass
     else:
          pass

     return market_dict



def completion_order(access_key,secret_key):
     user_balances  = all_accounts_exclude_krw_krw(access_key,secret_key)

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
               trade_price = current_qutation(market)
               if len(trade_price) == 0:
                    new_trade_price = 0
                    dt = new_trade_price - avg_buy_price
                    if dt == 0.0:
                         profit_rate = 0
                    else:
                         profit_rate = dt / avg_buy_price
                         
                    temp_dict['market'] = market
                    temp_dict['all_buy'] = all_buy
                    temp_dict['volume'] = volume
                    temp_dict['profit_rate'] = profit_rate * 100
                    completion_list.append(temp_dict)
               else:
                    new_trade_price = float(trade_price['trade_price'])
                    dt = new_trade_price - avg_buy_price
                    profit_rate = dt / avg_buy_price
                    temp_dict['market'] = market
                    temp_dict['all_buy'] = all_buy
                    temp_dict['volume'] = volume
                    temp_dict['profit_rate'] = profit_rate * 100
                    completion_list.append(temp_dict)
     return completion_list

def single_completion_order_rate(access_key,secret_key,market):

     
     user_balances  = all_accounts_exclude_krw_krw(access_key,secret_key)
     # print('user_balances 362',user_balances)
     for i in range(0,len(user_balances)):
          # print('i',i,user_balances[i]['market'])
          # print('market',market)
          if market == user_balances[i]['market']:
               # print(f"{market} == {user_balances[i]['market']}")
               temp_dict = dict()
               market = user_balances[i]['market']
               avg_buy_price =user_balances[i]['avg_buy_price']
               volume = user_balances[i]['all_volume']
               all_buy = user_balances[i]['all_buy']
               avg_buy_price = float(avg_buy_price)
               trade_price = current_qutation(market)
               new_trade_price = float(trade_price['trade_price'])
               dt = new_trade_price - avg_buy_price
               profit_rate = dt / avg_buy_price
               temp_dict['market'] = market
               temp_dict['all_buy'] = all_buy
               temp_dict['volume'] = volume
               temp_dict['profit_rate'] = profit_rate * 100
               return temp_dict
          # else:
          #      temp_dict = dict()
          #      return temp_dict


def swing_data_save(user_id,market,all_buy,volume,profit_rate):
     try:
          cur.execute("INSERT INTO swing(user_id,market,all_buy,volume,profit_rate) VALUES(%s,%s,%s,%s,%s)",(user_id,market,all_buy,volume,profit_rate))
     except  Exception as ex:
          print('swing_data_save err',ex)
          conn.rollback()
     else:
          conn.commit()
          
     return json.dumps({"result":"success"})

def swing_data_limit2(user_id,market):
     temp_list = list()
     market = 'KRW-ETH'
     try:
          cur.execute("select MAX(profit_rate), MIN(profit_rate) FROM swing WHERE user_id = %s AND market = %s",(user_id,market))
     except  Exception as ex:
          print('swing_data_save err',ex)
     else:
          temp_list = cur.fetchall()
          new_temp_list = list()
          for i in range(0,len(temp_list)):
               temp = dict()
               temp['max_profit_rate'] = temp_list[i][0]
               temp['min_profit_rate'] = temp_list[i][1]
               new_temp_list.append(temp)
               
     return new_temp_list 

def user_balance_check(access_key,secret_key):
     payload = {
     'access_key': access_key,
     'nonce': str(uuid.uuid4()),
     }

     jwt_token = jwt.encode(payload, secret_key)
     authorization = 'Bearer {}'.format(jwt_token)
     headers = {
     'Authorization': authorization,
     }

     res = requests.get(server_url + '/v1/accounts',headers=headers)
     res = res.json()

     return res

def current_market_tax_list(ticker_list):
     
     str_tickers = '%2C'.join(ticker_list)
     # print('str_tickers',str_tickers)
     url = f"https://api.upbit.com/v1/ticker?markets={str_tickers}"

     headers = {"Accept": "application/json"}

     
     cur_price_list = requests.get(url, headers=headers)
     cur_price_list = json.loads(cur_price_list.text)
     
     return cur_price_list

def db_balances_insert(market,all_buy,volume,profit_rate,market_trade_time,user_id):
     try:
          cur.execute('INSERT INTO balances(user_id,market,all_buy,volume,profit_rate,trade_time) VALUES(%s,%s,%s,%s,%s,%s)',(user_id,market,all_buy,volume,profit_rate,market_trade_time))
     except Exception as ex:
          print('db_balances_insert err',ex)
          conn.rollback()
     else:
          conn.commit()
          
     return 'success'


def db_balances_order_insert(market,volume,bid_price,profit_rate,market_trade_time,auto_set,user_id):

     try:
          cur.execute('INSERT INTO orders(user_id, market, volume, bid_price, profit_rate, work_time, auto_set) VALUES(%s,%s,%s,%s,%s,%s,%s)',(user_id,market,volume,bid_price,profit_rate,market_trade_time,auto_set))
     except Exception as ex:
          print('db_balances_order_insert err',ex)
          conn.rollback()
     else:
          conn.commit()
          
     return 'success'



def ask_list(user_id):
     try:
          # select market,max(work_time) from transactions where user_id = %s AND side = 'ask' AND work_time >= NOW() - INTERVAL '24 HOURS' GROUP BY market
          # cur.execute("select market,volume,price,work_time,uuid from transactions where user_id = %s AND side = 'ask' AND work_time >= NOW() - INTERVAL '24 HOURS' GROUP BY market",(user_id,))
          cur.execute("select market,volume,price,auto_set,work_time,uuid,side from transactions where (market, work_time) in (select market,max(work_time) as work_time from transactions where user_id = %s AND side = 'bid' AND work_time >= NOW() - INTERVAL '24 HOURS' group by market) order by market",(user_id,))
     except Exception as ex:
          print('ex',ex)
          conn.rollback()
     else:
          pass
          try:
               temp = cur.fetchall()
          except Exception as ex:
               print('ex2',ex)
               return {'result':'wait'}
          else:
               tempList = []
               markets = []
               for i in range(0,len(temp)):
                    temp_dict = dict()
                    temp_dict['market'] = temp[i][0]
                    temp_dict['volume'] = temp[i][1]
                    temp_dict['price'] = temp[i][2]
                    temp_dict['auto_set'] = temp[i][3]
                    work_time= temp[i][4]
                    temp_dict['work_time'] = work_time.strftime("%Y-%m-%d %H:%M:%S")
                    temp_dict['uuid'] = temp[i][5]
                    tempList.append(temp_dict)
               pass

     return tempList 