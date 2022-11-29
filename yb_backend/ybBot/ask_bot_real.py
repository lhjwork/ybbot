from commons.dbConnFetch import *
from commons.balance import *
from commons.price import *
from commons.quotation import * 
from commons.requests import *
from commons.split_panic import *

from datetime import datetime
from pytz import timezone, utc




KST = timezone('Asia/Seoul')
now = datetime.now(KST)

check_time = now.strftime('%H:%M:%S')



# 호가는 코인이 거래되는 가격의 단위 : 매매거래를 하기 위한 매도 또는 매수의 의사표시
# bid : 매수 / ask:매도
while(True):
     
     if '08:59:30' <= check_time <= '09:10:00':
          pass
          # print('우선 09:00:00 ~ 09:10:00에서 진입시도')
     else:
          # 전체 사용자 정보 조회\
               # 
          users = usersinfos()
          # print('users 31',users)
          # users :{'id': 1, 'invest_type': 'attack0', 'apikey': '111', 'secretkey': '111', 
          # 'panic_cell': 'step_one', 'seed_money': 332667.29934364,
          # 'entry_money': 99800.189803092}
          # users = sorted(users,key=itemgetter('id'))
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
               
               #자동매도
               # test = completion_order(user_accessKey,user_secretKey)
               entry_items = bid_history(user_accessKey,user_secretKey)
          
               # print('52',entry_items)
               # time.sleep(100)
               if entry_items == []:
                    pass
                    # print('failed no accesskey, secretkey')
               else:
                    # print('57')
                    # print('len',len(entry_items))
               # 자동매도
                    for k in range(0,len(entry_items)):
                         # print('k',k)
                         # print('entry_items 62',entry_items[k])
                         market = entry_items[k]['market']
                         volume = entry_items[k]['volume']
                         avg_bid_price = entry_items[k]['avg_bid_price']
                         profit_rate = entry_items[k]['profit_rate']
                         locked = entry_items[k]['locked']
                         if locked != '0':
                              pass
                         else:
                              profit_rate = float(profit_rate)
                              user_bid_data = select_recent_bid(user_id,market)
                              trade_price = current_trade_price(market)

                              try:
                                   panic_step = user_bid_data['panic_step']
                                   profit_rate
                              except Exception as ex:
                                   # print('panic_step err',ex)
                                   panic_step = None
                              else:
                                   pass
                                   # print('i',i)
                                   if panic_step == 'panic_four':
                                        if profit_rate <= -9.88:
                                             api_askPass(trade_price,volume,market,user_accessKey,user_secretKey,avg_bid_price,invest_type,user_id)
                                   else:
                                        
                                   # 상승장 익절
                                        if 30 <= profit_rate :
                                             api_askPass(trade_price,volume,market,user_accessKey,user_secretKey,avg_bid_price,invest_type,user_id)
                                   # 하락장 익절
                                        elif profit_rate <= -30:
                                             api_askPass(trade_price,volume,market,user_accessKey,user_secretKey,avg_bid_price,invest_type,user_id)

                                        else:
                                             # 자동매도
                                             #swing 계산
                                             # print('91',market)
                                             single_completion = single_completion_order_rate(user_accessKey,user_secretKey,market)
                                             # print('single_completion',single_completion)
                                             if len(single_completion) == 0:
                                                  pass
                                             else:
                                                  # time.sleep(2)
                                                  # print("single_completion['market']" ,single_completion['market'])
                                                  # time.sleep(2)
                                                  swing_data_save(user_id,single_completion['market'],single_completion['all_buy'],single_completion['volume'],single_completion['profit_rate'])
                                                  # time.sleep(1)
                                                  # print('97',swing_data_save)
                                                  
                                                  swing_data = swing_data_limit2(user_id,market)
                                                  # print('100',swing_data)
                                                  # time.sleep(200)
                                                  # print('swing_data',len(swing_data))
                                                  if len(swing_data) != 1:
                                                       pass
                                                  else:
                                                       # print('108')
                                                       profit_rate_1 = swing_data[0]['max_profit_rate']
                                                       profit_rate_2 = swing_data[0]['min_profit_rate']
                                                       profit_rate_1 = float(profit_rate_1)
                                                       profit_rate_2 = float(profit_rate_2)
                                                       # print('profit_rate_1',profit_rate_1)
                                                       # print('profit_rate_2',profit_rate_2)
                                                       # time.sleep(3)
                                                       ask_entry_count = auto_ask_entry(profit_rate_1)
                                                       # print('ask_entry_count',ask_entry_count)
                                                       swing_check = swing_entry(ask_entry_count,profit_rate_2,market)
                                                       # 
                                                       # print('swing_check',swing_check)
                                                       if swing_check == None:
                                                            pass
                                                       else:
                                                            if swing_check['result'] == 'success':
                                                                 api_askPass(trade_price,volume,market,user_accessKey,user_secretKey,avg_bid_price,invest_type,user_id)
                                                                 time.sleep(0.5)
                                                                 # api_askPass(trade_price,volume,market,user_accessKey,user_secretKey,avg_bid_price,user_id)
                                                            else:
                                                                 pass
                                                       
                    

                                             # ask_entry_count = auto_ask_entry(profit_rate)
                                        
                                        # swing_check = swing_entry(ask_entry_count,profit_rate,market)
                                        # if swing_check['result'] == 'success':
                                        #      api_askPass(trade_price,volume,market,user_accessKey,user_secretKey,avg_bid_price,user_id)
                                        # else:
                                        #      pass