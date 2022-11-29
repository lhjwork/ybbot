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
          # print('check_time',check_time)
          pass
          # print('우선 09:00:00 ~ 09:10:00에서 진입시도')
     else:
          # 전체 사용자 정보 조회
          users = usersinfos()
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

               # 수정 필요 진입 금액은 20000이어야 함
               if entry_money <= 20000 or not entry_money:
                    entry_money = 20000 
               
               if left_voucher == None or left_voucher <= 0:
                    pass
                    # print(f'해당 유저{user_id}는 남아있는 이용권이 없습니다.')
               else:
                    if entry_money == None:
                         entry_money = 0
                    else:
                         entry_money = float(entry_money)
                    
               
                         # print(f'test_user_id:{user_id}, entry_money 부족 현재 보유량:',entry_money)
                         # 하락장 특별매수 조건
                         
                         # user_bid_data = select_recent_bid(user_id,'KRW-CRE')
                    special_decrease_datas = rate_datas_special_decrease()
                    # print(len(special_decrease_datas))
                    # print('user_bid_data',user_bid_data)
                    if len(special_decrease_datas) != 0:
                         for k in range(0,len(special_decrease_datas)):
                              entry_market = special_increase_datas[k]['market']
                              change_rate = special_increase_datas[k]['change_rate']
                              user_bid_data = select_recent_bid(user_id,entry_market)
                              single_completion = single_completion_order_rate(user_accessKey,user_secretKey,entry_market)
                                   
                              
                              if len(single_completion) == 0:
                                   profit_rate = 0.0
                              else:
                                   
                                   profit_rate = single_completion['profit_rate']
                              # print('user_bid_data',user_bid_data)
                              try:
                                   split_step = user_bid_data['split_one']
                                   panic_step = user_bid_data['panic_step']
                              except Exception as ex:
                                   # print('panic_step err',ex)
                                   panic_step = None
                                   split_step = None
                              else:
                                   pass
                              # 데이터 없을 시 최초 구매 
                              if len(user_bid_data) == 0:
                                   if -65 <= change_rate <= -56:
                                        split_step = 'special'
                                        panic_step = 'special'
                                        api_bidPass(entry_money*4,entry_market,user_accessKey,user_secretKey,split_step,panic_step,'하락장특별매수',user_id)
                                        
                                   elif -56 <= change_rate <= -46:
                                        split_step = 'special'
                                        panic_step = 'special'
                                        api_bidPass(entry_money*3,entry_market,user_accessKey,user_secretKey,split_step,panic_step,'하락장특별매수',user_id)
                                   elif -46 <= change_rate <= -36:
                                        split_step = 'special'
                                        panic_step = 'special'
                                        api_bidPass(entry_money*2,entry_market,user_accessKey,user_secretKey,split_step,panic_step,'하락장특별매수',user_id)
                                   elif -36 <= change_rate <= -25:   
                                        split_step = 'special'
                                        panic_step = 'special'
                                        api_bidPass(entry_money*1,entry_market,user_accessKey,user_secretKey,split_step,panic_step,'하락장특별매수',user_id)
                              else:
                                   if split_step == 'special':
                                        # user_completion_order
                                        
                                        # print('상승장 진입한 값이 있을 때')
                                        # change_rate 필요
                                        # panic_bid_real(entry_market,entry_money,panic_step,profit_rate,user_accessKey,user_secretKey,'하락장특별매수',user_id)
                                        pass
                                        
                                             
                    # 상승장 특별매수 
                    # rate_datas_special_increase() temp_dict return market, change_rate, update_time, invest_type
                    special_increase_datas = rate_datas_special_increase()
                    if len(special_increase_datas) != 0:
                         # print('상승장 특별매수 존재')
                         # rate_datas_special_increase() temp_dict return market, change_rate, update_time, invest_type
                         for k in range(0,len(special_increase_datas)):
                              entry_market = special_increase_datas[k]['market']
                              change_rate = special_increase_datas[k]['change_rate']
                              user_bid_data = select_recent_bid(user_id,entry_market)
                              single_completion = single_completion_order_rate(user_accessKey,user_secretKey,entry_market)
                              if len(single_completion) == 0:
                                   profit_rate = 0.0
                              else:
                                   profit_rate = single_completion['profit_rate']
                              try:
                                   split_step = user_bid_data['split_one']
                                   panic_step = user_bid_data['panic_step']
                              except Exception as ex:
                                   # print('panic_step err',ex)
                                   panic_step = None
                                   split_step = None
                              else:
                                   pass
                              # 사용자 매수 데이터가 없을 시 패닉세 자동 투자
                              if len(user_bid_data) == 0:
                                   # 매수총액 x1 = seed_money / 100 
                                   # 상승코인 60% + 3% 이상시 불장 1단계 => 매수총액 x1 배수 매수 ( 분할매수기능 작동안함 / 패닉셀 매수기능 작동함 )
                                   # panic_bid_real(entry_item,entry_money,accessKey,secretKey,user_id)
                                   # 최초 매수 시도
                                   if 9 <= change_rate:
                                        split_step = 'special'
                                        panic_step = 'special'
                                        api_bidPass(entry_money*4,entry_market,user_accessKey,user_secretKey,split_step,panic_step,'상승장특별매수',user_id)
                                   elif 7 <= change_rate:
                                        split_step = 'special'
                                        panic_step = 'special'
                                        api_bidPass(entry_money*3,entry_market,user_accessKey,user_secretKey,split_step,panic_step,'상승장특별매수',user_id)
                                   elif 5 <= change_rate:
                                        split_step = 'special'
                                        panic_step = 'special'
                                        api_bidPass(entry_money*2,entry_market,user_accessKey,user_secretKey,split_step,panic_step,'상승장특별매수',user_id)
                                   elif 3 <= change_rate:
                                        split_step = 'special'
                                        panic_step = 'special'
                                        api_bidPass(entry_money*1,entry_market,user_accessKey,user_secretKey,split_step,panic_step,'상승장특별매수',user_id)
                              else:
                                   if split_step == 'special':
                                        # 상승장 특별 매수 
                                        # print('상승장 진입한 값이 있을 때')
                                        # panic_bid_real(entry_market,entry_money,panic_step,user_accessKey,user_secretKey,'상승장특별매수',user_id)
                                        pass                  
                    else:
                         # invest_type : attack0 2초 2%급등
                         if invest_type == 'attack0':
                              default_rate_datas = rate_datas_default()
               
                              # print('default_rate_datas',default_rate_datas)
                              # default_rate_datas dict return key --> market,change_rate, update_time, invest_type
                              for i in range(0,len(default_rate_datas)):
               
                                   entry_market = default_rate_datas[i]['market']
                                   change_rate = default_rate_datas[i]['change_rate']
                                   single_completion = single_completion_order_rate(user_accessKey,user_secretKey,entry_market)
                                   split_step = 'split_one'
                                   panic_step = None
                                   
                                   if len(single_completion) == 0:
                                        # 최초 매수 시도
                                        split_step = 'split_one'
                                        panic_step = None
                                        test = api_bidPass(entry_money* 0.3,entry_market,user_accessKey,user_secretKey,split_step,panic_step,invest_type,user_id)
                                        # print('test',test)
                                        pass
                                   else:
                                        pass
                                        # profit_rate = single_completion['profit_rate']
                                        # user_bid_data = select_recent_bid(user_id,entry_market)

                                        # split_step = user_bid_data['split_step']
                                        # panic_step = user_bid_data['panic_step']
                                        # # 사용자 매수 데이터가 있을 때는 1차 매수가 들어 갔음
                                        # if len(user_bid_data) != 0:
                                        #      # 중복 매수를 확인하고
                                        #      # 분할 매수3차 까지 이루지면 split_one,panic_one으로 db 반영되서 매수 진입
                                        #      # print('entry_market',entry_market)
                                        #      # print('split_step',split_step)
                                        #      # print('panic_step',panic_step)
                                        #      if split_step == 'split_one':
                                        #           # 분할 매수 및 패닉셀 매수 진입로직
                                        #           result = split_panic_bid_real(entry_market,entry_money,user_accessKey,user_secretKey,profit_rate,split_step,panic_step,invest_type,user_id)
                                        #           # print('기본 분할 매수 및 패닉셀 매수 결과',result['result'])
                                        #      elif split_step == 'split_two':
                                        #           # 분할 매수 및 패닉셀 매수 진입로직
                                        #           result = split_panic_bid_real(entry_market,entry_money,user_accessKey,user_secretKey,profit_rate,split_step,panic_step,invest_type,user_id)
                                                  
                                        #           # print('기본 분할 매수 및 패닉셀 매수 결과',result['result'])
                                        #      elif split_step == 'split_three':
                                        #           # 분할 매수 및 패닉셀 매수 진입로직
                                        #           result = split_panic_bid_real(entry_market,entry_money,user_accessKey,user_secretKey,profit_rate,split_step,panic_step,invest_type,user_id)
                                        #           # print('기본 분할 매수 및 패닉셀 매수 결과',result['result'])
                                        
                                        
                         if invest_type == 'attack1':
                              default_rate_datas = rate_datas_attack1()
                              # default_rate_datas dict return key --> market,change_rate, update_time, invest_type
                              # print('default_rate_datas',default_rate_datas)
                              # default_rate_datas dict return key --> market,change_rate, update_time, invest_type
                              # print('default_rate_datas',default_rate_datas)
                              for i in range(0,len(default_rate_datas)):
                                   # print('entry_market',i)
                                   entry_market = default_rate_datas[i]['market']
                                   # print('entry_market',entry_market)
                                   change_rate = default_rate_datas[i]['change_rate']
                                   single_completion = single_completion_order_rate(user_accessKey,user_secretKey,entry_market)
                                   # print('single_completion',single_completion)
                                   
                                   if len(single_completion) == 0:
                                        # 최초 매수 시도
                                        split_step = 'split_one'
                                        panic_step = None
                                        test = api_bidPass(entry_money* 0.3,entry_market,user_accessKey,user_secretKey,split_step,panic_step,invest_type,user_id)
                                        # print('test',test)
                                        pass
                                   else:
                                        pass
                                        
                         
                         if invest_type == 'attack2':
                              default_rate_datas = rate_datas_attack2()
                              # default_rate_datas dict return key --> market,change_rate, update_time, invest_type
                              # print('default_rate_datas',default_rate_datas)
                              # default_rate_datas dict return key --> market,change_rate, update_time, invest_type
                              for i in range(0,len(default_rate_datas)):
               
                                   entry_market = default_rate_datas[i]['market']
                                   change_rate = default_rate_datas[i]['change_rate']
                                   single_completion = single_completion_order_rate(user_accessKey,user_secretKey,entry_market)
                                   if len(single_completion) == 0:
                                        # 최초 매수 시도
                                        split_step = 'split_one'
                                        panic_step = None
                                        test = api_bidPass(entry_money* 0.3,entry_market,user_accessKey,user_secretKey,split_step,panic_step,invest_type,user_id)
                                        # print('test',test)
                                        pass
                                   else:
                                        pass
                                   
                                   
                         if invest_type == 'shield0':
                              default_rate_datas = rate_datas_shield0()
                              
                              for i in range(0,len(default_rate_datas)):
                                   # print('entry_market',i)
                                   entry_market = default_rate_datas[i]['market']
                                   # print('entry_market',entry_market)
                                   change_rate = default_rate_datas[i]['change_rate']
                                   single_completion = single_completion_order_rate(user_accessKey,user_secretKey,entry_market)
                                   # print('single_completion',single_completion)
                                   
                                   if len(single_completion) == 0:
                                        # 최초 매수 시도
                                        split_step = 'split_one'
                                        panic_step = None
                                        test = api_bidPass(entry_money*0.3 ,entry_market,user_accessKey,user_secretKey,split_step,panic_step,invest_type,user_id)
                                        # print('test',test)
                                        pass
                                   else:
                                        pass
                                   
                                   
                         if invest_type == 'shield1':
                              default_rate_datas = rate_datas_shield1()
                              # default_rate_datas dict return key --> market,change_rate, update_time, invest_type
                              # print('default_rate_datas',default_rate_datas)
                              # default_rate_datas dict return key --> market,change_rate, update_time, invest_type
                              # print('default_rate_datas',default_rate_datas)
                              for i in range(0,len(default_rate_datas)):
                                   # print('entry_market',i)
                                   entry_market = default_rate_datas[i]['market']
                                   # print('entry_market',entry_market)
                                   change_rate = default_rate_datas[i]['change_rate']
                                   single_completion = single_completion_order_rate(user_accessKey,user_secretKey,entry_market)
                                   # print('single_completion',single_completion)
                                   
                                   if len(single_completion) == 0:
                                        # 최초 매수 시도
                                        split_step = 'split_one'
                                        panic_step = None
                                        test = api_bidPass(entry_money* 0.3,entry_market,user_accessKey,user_secretKey,split_step,panic_step,invest_type,user_id)
                                        # print('test',test)
                                        pass
                                   else:
                                        pass
                                   
                                   
                         if invest_type == 'shield2':
                              default_rate_datas = rate_datas_shield2()
                              # default_rate_datas dict return key --> market,change_rate, update_time, invest_type
                              # print('default_rate_datas',default_rate_datas)
                              # default_rate_datas dict return key --> market,change_rate, update_time, invest_type
                              # print('default_rate_datas',default_rate_datas)
                              for i in range(0,len(default_rate_datas)):
                                   # print('entry_market',i)
                                   entry_market = default_rate_datas[i]['market']
                                   # print('entry_market',entry_market)
                                   change_rate = default_rate_datas[i]['change_rate']
                                   single_completion = single_completion_order_rate(user_accessKey,user_secretKey,entry_market)
                                   # print('single_completion',single_completion)
                                   
                                   if len(single_completion) == 0:
                                        # 최초 매수 시도
                                        split_step = 'split_one'
                                        panic_step = None
                                        test = api_bidPass(entry_money* 0.3,entry_market,user_accessKey,user_secretKey,split_step,panic_step,invest_type,user_id)
                                        # print('test',test)
                                        pass
                                   else:
                                        pass
                                   
                         # if invest_type == 'shield1':
                         #      print('rsi 매수 시점')
                                        # profit_rate = single_completion['profit_rate']
                                        # user_bid_data = select_recent_bid(user_id,entry_market)

                                        # split_step = user_bid_data['split_step']
                                        # panic_step = user_bid_data['panic_step']
                                        # # 사용자 매수 데이터가 있을 때는 1차 매수가 들어 갔음
                                        # if len(user_bid_data) != 0:
                                        #      # 중복 매수를 확인하고
                                        #      # 분할 매수3차 까지 이루지면 split_one,panic_one으로 db 반영되서 매수 진입
                                        #      # print('entry_market',entry_market)
                                        #      # print('split_step',split_step)
                                        #      # print('panic_step',panic_step)
                                        #      if split_step == 'split_one':
                                        #           # 분할 매수 및 패닉셀 매수 진입로직
                                        #           result = split_panic_bid_real(entry_market,entry_money,user_accessKey,user_secretKey,profit_rate,split_step,panic_step,invest_type,user_id)
                                        #           # print('기본 분할 매수 및 패닉셀 매수 결과',result['result'])
                                        #      elif split_step == 'split_two':
                                        #           # 분할 매수 및 패닉셀 매수 진입로직
                                        #           result = split_panic_bid_real(entry_market,entry_money,user_accessKey,user_secretKey,profit_rate,split_step,panic_step,invest_type,user_id)
                                                  
                                        #           # print('기본 분할 매수 및 패닉셀 매수 결과',result['result'])
                                        #      elif split_step == 'split_three':
                                        #           # 분할 매수 및 패닉셀 매수 진입로직
                                        #           result = split_panic_bid_real(entry_market,entry_money,user_accessKey,user_secretKey,profit_rate,split_step,panic_step,invest_type,user_id)
                                        #           # print('기본 분할 매수 및 패닉셀 매수 결과',result['result'])
                                        