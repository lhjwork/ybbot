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
          # 전체 사용자 정보 조회
          users = usersinfos()
          user_accessKey = 'xxrHjO3rbgxjYCIHxj1nDmR3oxPyCO126j4LlhkX'
          user_secretKey = 'gRFkcQp8sz4tERMEeiwgmM2BC2F4WgfxxnJodCQu'
          single_completion = single_completion_order_rate(user_accessKey,user_secretKey,'KRW-HUNT')
          # print('single_completion',single_completion)
          volume = single_completion['volume']
          trade_price = current_trade_price('KRW-HUNT')
          test = api_askPass(trade_price,volume,'KRW-HUNT',user_accessKey,user_secretKey,0.0,'attact1',1)

          # api_askPass(trade_price,volume,market,user_accessKey,user_secretKey,avg_bid_price,invest_type,user_id)
               # # print('test',test)
          time.sleep(100)

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
               trade_price = current_trade_price('KRW-BTT')
               
               # print('trade_price',price)
               # # time.sleep(100)
               # # user_balances  = all_accounts_exclude_krw_krw(user_accessKey,user_secretKey)
               # # api_askPass(trade_price,volume,ticker,accessKey,secretKey,avg_bid_price,invest_type,user_id)
               # # test = api_askPass(price,3.58306188,'KRW-CHZ',user_accessKey,user_secretKey,1535,invest_type,user_id)
               # api_askPass(trade_price,volume,market,user_accessKey,user_secretKey,avg_bid_price,invest_type,user_id)
               # # print('test',test)
               # time.sleep(100)