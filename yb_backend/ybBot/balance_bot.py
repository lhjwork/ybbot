from ast import While
import requests
import json
from commons.quotation import quo_orderbook
from commons.dbConnFetch import *
from commons.balance import *
from commons.price import *
from operator import itemgetter
from commons.checkStock import view_krw_items
from commons.requests import *
from commons.quotation import * 
from commons.split_panic import *

import time
from datetime import datetime
from pytz import timezone, utc








KST = timezone('Asia/Seoul')
now = datetime.now(KST)

check_time = now.strftime('%H:%M:%S')

# print('check_time',check_time)

conn = dbConn_no_cur()
cur = conn.cursor()

# 호가는 코인이 거래되는 가격의 단위 : 매매거래를 하기 위한 매도 또는 매수의 의사표시
# bid : 매수 / ask:매도
while(True):
     
     users = lookup_userKey()
     krw_ticker_list = view_krw_items()
     # print('41',krw_ticker_list)
     # print('users',users)
     users_keyList = []
     for i in range(0,len(users)):
          temp = dict()
          user_id = users[i]['id']
          access_key = users[i]['access_key']
          secret_key = users[i]['secret_key']
          # if user_id != 1:
                    
          if access_key == None or secret_key == None:
               pass
               # print(f'user_id:{user_id}는 accessKey,secretKey 등록 필요')
          else:
               balance = seed_status(access_key,secret_key)
               if type(balance) != type(dict()):
                    seed_money = balance[0]['seed_money']
                    seed_money = float(seed_money)
                    # entry_money = seed_money / 100
                    # seed 머니 100만원 기준 1/50로 제한
                    entry_money = seed_money / 50
                    result_save_currency = save_currency(seed_money,entry_money,user_id)
          # # else:
          #      if access_key == None or secret_key == None:
          #           pass

          #           # print(f'user_id:{user_id}는 accessKey,secretKey 등록 필요')
          #      else:
                    # print('user_id',user_id)
                    # print('access_key',access_key,secret_key)
                    balance = seed_status(access_key,secret_key)
                    print('71', type(balance))
                    if type(balance) != type(dict()):
                         
                         seed_money = balance[0]['seed_money']
                         
                         seed_money = float(seed_money)
                         
                         entry_money = seed_money*0.3
                         
                         try:
                              time.sleep(1)
                              save_currency(seed_money,entry_money,user_id)
                         except Exception as ex:
                              print('save_currency err',ex)
                         else:
                              # user가 가지고 있는 종목의 현재 값 전체 확인
                              user_balances = user_balance_check(access_key,secret_key)
                              # print('user_balances 87',user_balances)
                              ticker_list = []
                              # 업비트에 현재 등록되 krw만 정제
                              
                              for i in range(0,len(user_balances)):
                                   currency = user_balances[i]['currency']
                                   unit_currency = user_balances[i]['unit_currency']
                                   if unit_currency != 'KRW' or currency == 'KRW':
                                        pass
                                   else:
                                        ticker = unit_currency + '-' + currency
                                        for k in range(0,len(krw_ticker_list)):
                                             # user balance에 해당하는 tikcer만 list에 담음
                                             if ticker == krw_ticker_list[k]:
                                                  ticker_list.append(ticker)
                              
                                                  
                              cur_trade_maket_list = []
                              # print('user_balancesuser_balancesuser_balances',user_balances)
                              for i in range(0,len(user_balances)):
                                   currency = user_balances[i]['currency']
                                   unit_currency = user_balances[i]['unit_currency']
                                   if unit_currency != 'KRW' or currency == 'KRW':
                                        pass
                                   else:
                                        for k in range(0,len(krw_ticker_list)):
                                             ticker = unit_currency + '-' + currency
                                             if ticker == krw_ticker_list[k]:
                                                  temp = dict()
                                                  temp['market'] = ticker
                                                  temp['balance'] = user_balances[i]['balance']
                                                  temp['avg_buy_price'] = user_balances[i]['avg_buy_price']
                                                  # temp['locked'] = user_balances[i]['locked']
                                                  cur_trade_maket_list.append(temp)
                              
                                        
                              #현재 시세 조회 
                              tax_list = current_market_tax_list(ticker_list)
                              # print('tax_list--->',tax_list)
                              for i in range(0,len(cur_trade_maket_list)):
                                   market = cur_trade_maket_list[i]['market']
                                   balance = cur_trade_maket_list[i]['balance']
                                   avg_buy_price = cur_trade_maket_list[i]['avg_buy_price']
                                   # locked = cur_trade_maket_list[i]['locked']
                                   for k in range(0,len(tax_list)):
                                        if market == tax_list[k]['market']:
                                             # print('market',market)
                                             balance = cur_trade_maket_list[k]['balance']
                                             avg_buy_price = cur_trade_maket_list[k]['avg_buy_price']
                                             bid_value = float(balance) * float(avg_buy_price)
                                             # print('bid_value 134',bid_value)
                                             trade_price = tax_list[k]['trade_price']
                                             # print('trade_price',trade_price)
                                             trade_date_kst = tax_list[k]['trade_date_kst']
                                             trade_time_kst = tax_list[k]['trade_time_kst']
                                             market_trade_time = trade_date_kst+' '+trade_time_kst
                                             market_trade_time = datetime.strptime(market_trade_time,'%Y%m%d %H%M%S')
                                             cur_value = float(balance) * float(trade_price)
                                             # print('cur_value 142',cur_value)
                                             try:
                                                  profit_rate = (cur_value - bid_value) * 100 / bid_value
                                             except:
                                                  profit_rate = -30
                                             else:
                                                  pass
                                                  
                                             # 거래완료에서 완료 부분 내역 저장
                                             # print('140',market,bid_value,balance,profit_rate,market_trade_time,user_id)
                                             db_balances_insert(market,bid_value,balance,profit_rate,market_trade_time,user_id)
                                             # time.sleep(1)
                                             
                              
                              bid_list_24hour  = ask_list(user_id)
                              recent_order_tickers = list()
                              for i in range(0,len(bid_list_24hour)):
                                   market = bid_list_24hour[i]['market']
                                   for k in range(0,len(krw_ticker_list)):
                                        # user balance에 해당하는 tikcer만 list에 담음
                                        if market == krw_ticker_list[k]:
                                             recent_order_tickers.append(market)
                                             
                              tax_list = current_market_tax_list(recent_order_tickers)
                              
                              
                              for i in range(0,len(bid_list_24hour)):
                                   temp_dict = dict()
                                   market = bid_list_24hour[i]['market']
                                   for k in range(0,len(tax_list)):
                                        if market == tax_list[k]['market']:
                                             volume = bid_list_24hour[i]['volume']
                                             user_trade_price = bid_list_24hour[i]['price']
                                             auto_set = bid_list_24hour[i]['auto_set']
                                             work_time = bid_list_24hour[i]['work_time']
                                             trade_price = tax_list[k]['trade_price']
                                             trade_volume = tax_list[k]['trade_volume']
                                             trade_date_kst = tax_list[k]['trade_date_kst']
                                             trade_time_kst = tax_list[k]['trade_time_kst']
                                             user_bid_value = float(user_trade_price) / float(volume)
                                             cur_bid_value = float(trade_price)
                                             profit_rate = (cur_bid_value - user_bid_value) * 100 / user_bid_value

                                             db_balances_order_insert(market,volume,user_trade_price,profit_rate,work_time,auto_set,user_id)

          time.sleep(0.5)
                                             
                    
               
                    