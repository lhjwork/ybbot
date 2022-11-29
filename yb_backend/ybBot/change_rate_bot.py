from commons.dbConnFetch import *
from commons.quotation import *
from commons.checkStock import view_krw_items
from commons.balance import *
import requests
import time
# 
while True:
     test_1 = ''
     test_2 = ''
     ticker_list = view_krw_items()
     str_tickers = '%2C'.join(ticker_list)
     
     url = f"https://api.upbit.com/v1/ticker?markets={str_tickers}"

     headers = {"Accept": "application/json"}
#1. 전체 조회
     price_check_1 = requests.get(url, headers=headers)
     price_check_1 = json.loads(price_check_1.text)
     # print('price_check_1')
     time.sleep(2)
#1. 전체 조회 
     price_check_2 = requests.get(url, headers=headers)
     price_check_2 = json.loads(price_check_2.text)
     # print('price_check_2')
     time.sleep(1)
     
     price_check_3 = requests.get(url, headers=headers)
     price_check_3 = json.loads(price_check_3.text)
     # print('price_check_3')
     time.sleep(2)
     
     price_check_4 = requests.get(url, headers=headers)
     price_check_4 = json.loads(price_check_4.text)
     # print('price_check_4',price_check_4)
     
     time.sleep(2)
     # 상승장 특별 매수 셋팅
     len_all= len(ticker_list)
     increase_list = list()
     for i in range(0,len(ticker_list)):
          tickr_info_dict = dict()
          new_tickets_1 = price_check_1[i]
          new_tickets_2 = price_check_2[i]
          price_dt_default = new_tickets_2['trade_price'] - new_tickets_1['trade_price']
          percentage_default = price_dt_default / new_tickets_1['trade_price']
          percentage_default = percentage_default * 100
          signed_change_rate = new_tickets_1['signed_change_rate'] * 100
          if 0 < percentage_default:
               market = new_tickets_2['market']
               increase_list.append(market)
     
     # 하락장 특별매수 부분
     # rate table type decrease1,decrease2,decrease3,decrease4
     len_all= len(ticker_list)
     decrease_list = list()
     for i in range(0,len(ticker_list)):
          tickr_info_dict = dict()
          new_tickets_1 = price_check_1[i]
          new_tickets_2 = price_check_2[i]
          price_dt_default = new_tickets_2['trade_price'] - new_tickets_1['trade_price']
          percentage_default = price_dt_default / new_tickets_1['trade_price']
          # 상승중인지 계산
          percentage_default = percentage_default * 100
          # 전일 종가 대비 변화율
          signed_change_rate = new_tickets_1['signed_change_rate'] * 100
          
          if -65 <= signed_change_rate <= -56:
               print('하락장특별매수 진입67')
               if 2 < percentage_default:
                    market = new_tickets_2['market']
                    trade_price = new_tickets_2['trade_price']
                    decrease_special_invest_save(market,trade_price,percentage_default,"decrease")
          elif -56 <= signed_change_rate <= -46:
               print('하락장특별매수 진입73')
               if 2 < percentage_default:
                    market = new_tickets_2['market']
                    trade_price = new_tickets_2['trade_price']
                    decrease_special_invest_save(market,trade_price,percentage_default,"decrease")
          elif -46 <= signed_change_rate <= -36:
               if 2 < percentage_default:
                    print('하락장특별매수 진입80')
                    market = new_tickets_2['market']
                    trade_price = new_tickets_2['trade_price']
                    decrease_special_invest_save(market,trade_price,percentage_default,"decrease")
          elif -36 <= signed_change_rate <= -25:
               print('하락장특별매수 진입85')
               if 2 < percentage_default:
                    market = new_tickets_2['market']
                    trade_price = new_tickets_2['trade_price']
                    decrease_special_invest_save(market,trade_price,percentage_default,"decrease")
     
     
     # print('market-===>',new_tickets_2['market'])
     # print('signed_change_rate=====>',signed_change_rate)
     
     # 상승장 특별매수를 위한 60% 비율 확인 계산
     increasing_rate = len(increase_list) / len_all
     # 상승장 특별매수 market 별 data commit -> invest 하는 bot 부분에서 활용가능한
     # special(invest_type)에서 데이터 매매 시도
     if 60 <= increasing_rate:
          # print('상승장특별매수 진입')
          for i in range(0,len(ticker_list)):
               tickr_info_dict = dict()
               new_tickets_1 = price_check_1[i]
               new_tickets_2 = price_check_2[i]
               price_dt_default = new_tickets_2['trade_price'] - new_tickets_1['trade_price']
               percentage_default = price_dt_default / new_tickets_1['trade_price']
               percentage_default = percentage_default * 100
               market = new_tickets_2['market']
               trade_price = new_tickets_2['trade_price']
               
          if 3 <= percentage_default:
               try:
                    cur.execute("INSERT INTO rate(market,trade_price,change_rate,type) VALUES(%s,%s,%s,%s)",(market,trade_price,percentage_default,'special'))
               except Exception as ex:
                    # print('isert into rate err',ex)
                    conn.rollback()
               else:
                    conn.commit()
     else:
          pass
          # print("=============================================================================")
          # print(price_check_2.text)
          new_ticker_info_list = list()
          for i in range(0,len(ticker_list)):
               tickr_info_dict = dict()
               new_tickets_1 = price_check_1[i]
               new_tickets_2 = price_check_2[i]
               new_tickets_3 = price_check_3[i]
               new_tickets_4 = price_check_4[i]

               price_dt_default = new_tickets_2['trade_price'] - new_tickets_1['trade_price']
               price_dt_attackOne = new_tickets_3['trade_price'] - new_tickets_1['trade_price']
               price_dt_attackTwo = new_tickets_4['trade_price'] - new_tickets_1['trade_price']
          
               percentage_default = price_dt_default / new_tickets_1['trade_price']
               percentage_attackOne = price_dt_attackOne / new_tickets_1['trade_price']
               percentage_attackTwo = price_dt_attackTwo / new_tickets_1['trade_price']
               percentage_default = percentage_default * 100
               percentage_attackOne = percentage_default * 100
               percentage_attackTwo = percentage_default * 100
               
               if 2 < percentage_default:
                    market = new_tickets_2['market']
                    trade_price = new_tickets_2['trade_price']
                    
                    try:
                         cur.execute("INSERT INTO rate(market,trade_price,change_rate,type) VALUES(%s,%s,%s,%s)",(market,trade_price,percentage_default,'attack0'))
                    except Exception as ex:
                         # print('ex err',ex)
                         conn.rollback()
                    else:
                         conn.commit()
               
               if 3 < percentage_attackOne:
                    market = new_tickets_3['market']
                    trade_price = new_tickets_3['trade_price']
                    
                    try:
                         cur.execute("INSERT INTO rate(market,trade_price,change_rate,type) VALUES(%s,%s,%s,%s)",(market,trade_price,percentage_attackOne,'attack1'))
                    except Exception as ex:
                         # print('ex err',ex)
                         conn.rollback()
                    else:
                         conn.commit()

               
               if 5 < percentage_attackTwo:
                    market = new_tickets_4['market']
                    trade_price = new_tickets_4['trade_price']
                    
                    try:
                         cur.execute("INSERT INTO rate(market,trade_price,change_rate,type) VALUES(%s,%s,%s,%s)",(market,trade_price,percentage_attackTwo,'attack2'))
                    except Exception as ex:
                         # print('ex err',ex)
                         conn.rollback()
                    else:
                         conn.commit()
          #2. 시세 비교 -> 2%상승 market 조회
          #3. 해당 market 시세 및 ticker 전달
          #SELECT market, change_rate, update_time,type FROM  rate WHERE (market,update_time) IN (select market,max(update_time) FROM rate WHERE update_time >= NOW() - INTERVAL '60 SECONDS' GROUP BY market) ORDER BY update_time DESC

          #ask에서 매수 시도