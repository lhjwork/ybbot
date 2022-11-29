from commons.dbConnFetch import *
from commons.balance import *
from commons.price import *
from commons.quotation import * 
from commons.requests import *
from commons.split_panic import *
from commons.checkStock import view_krw_items

from datetime import datetime
from pytz import timezone, utc



KST = timezone('Asia/Seoul')
now = datetime.now(KST)

check_time = now.strftime('%H:%M:%S')




# 호가는 코인이 거래되는 가격의 단위 : 매매거래를 하기 위한 매도 또는 매수의 의사표시
# bid : 매수 / ask:매도
while(True):
     
     if '08:59:30' <= check_time <= '09:10:00':
          # print('check_time',check_time)
          pass
          # print('우선 09:00:00 ~ 09:10:00에서 진입시도')
     else:
          # 전체 사용자 정보 조회
          try:
               users = usersinfos()
          except Exception as ex:
               print('users = usersinfos() err',ex)
          else:
               pass
          try:
               krw_ticker_list = view_krw_items()
          except Exception as ex:
               print('krw_ticker_list = view_krw_items()',ex)
          else:
               pass
          # print('krw_ticker_list',krw_ticker_list)
          # users :{'id': 1, 'invest_type': 'attack0', 'apikey': '111', 'secretkey': '111', 
          # 'panic_cell': 'step_one', 'seed_money': 332667.29934364,
          # 'entry_money': 99800.189803092}
          # users = sorted(users,key=itemgetter('id'))
          # print('users',users)
          for i in range(0,len(users)):
               user_id = users[i]['id']
               # invest_type : attack0, attack1, attack2
               invest_type = users[i]['invest_type']
               user_accessKey = users[i]['apikey']
               user_secretKey = users[i]['secretkey']
               panic_cell = users[i]['panic_cell']
               seed_money = users[i]['seed_money']
               entry_money = users[i]['entry_money']
               left_voucher = user_left_voucher(user_id)
               # user_balances  = all_accounts_exclude_krw_krw(user_accessKey,user_secretKey)
               
               user_balances = user_balance_check(user_accessKey,user_secretKey)

               ticker_list = []
               # 업비트에 현재 등록되 krw만 정제
               # print('user_balances',user_balances)
               for i in range(0,len(user_balances)):
                    currency = user_balances[i]['currency']
                    unit_currency = user_balances[i]['unit_currency']
                    avg_buy_price = user_balances[i]['avg_buy_price']
                    balance = user_balances[i]['balance']
                    locked = user_balances[i]['locked']
                    
                    
                    if unit_currency != 'KRW' or currency == 'KRW':
                         pass
                    elif locked != '0':
                         # print('ticker currency',currency)
                         pass
                    else:
                         ticker = unit_currency + '-' + currency
                         for k in range(0,len(krw_ticker_list)):
                              # user balance에 해당하는 tikcer만 list에 담음
                              if ticker == krw_ticker_list[k]:
                                   # print('ticker 분할 매수 확인 지점 진입',ticker)
                                   profit_rate = market_profit_rate_search(user_id, ticker)
                                   entry_market = krw_ticker_list[k]

                                   # 수정 필요 진입 금액은 20000이어야 함
                                   if entry_money < 6000 or not entry_money:
                                        pass
                                   else:
                                        user_bid_data = select_recent_bid(user_id,entry_market)
                                        if len(user_bid_data) == 0:
                                             pass
                                        else:
                                             # print('user_bid_data',user_bid_data)
                                             # time.sleep(10)
                                             split_step = user_bid_data['split_step']
                                             panic_step = user_bid_data['panic_step']
                                             traded_price = user_bid_data['traded_price']
                                             # 사용자 매수 데이터가 있을 때는 1차 매수가 들어 갔음
                                             if len(user_bid_data) != 0:
                                                  # print('84 entry_market',entry_market)
                                                  # print('85 traded_price',traded_price)
                                                  # print('86 profit_rate',profit_rate)
                                                  # print('87 split_step',split_step)
                                                  # print('88 panic_step',panic_step)
                                                  # print('89 user_id',user_id)
                                                  # time.sleep(3)
                                                  result = split_panic_bid_real(entry_market,traded_price,user_accessKey,user_secretKey,profit_rate,split_step,panic_step,invest_type,balance,avg_buy_price,user_id)
                                                  # print('result',result)
                                             else:
                                                  pass