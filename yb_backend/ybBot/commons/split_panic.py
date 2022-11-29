from commons.requests import *
from commons.dbConnFetch import *


def split_bid(entry_items,entry_money,accessKey,secretKey,user_id):
     for i in range(0,len(entry_items)):
          en_market = entry_items[i]['market']
          en_profit_rate = entry_items[i]['profit_rate']
          en_profit_rate = float(en_profit_rate)
          # 방어률 -18.0에 도달 했을 때

          user_bid_data = select_recent_bid(user_id,en_market)
          split_step = user_bid_data['split_step']
          # panic_step = user_bid_data['panic_step']

          # 방어률 -18.0에 도달 했을 때, split_two 진행
          if split_step == 'split_one':
               if en_profit_rate <= -18.0:
                    return api_bidPass(entry_money*0.3,en_market,accessKey,secretKey,'split_two',None,user_id)
               else:
                    return {'result':'wait'}
          if split_step == 'split_two':
               if en_profit_rate <= -9.0:
                    return api_bidPass(entry_money*0.4,en_market,accessKey,secretKey,'split_three',None,user_id)
               else:
                    return {'result':'wait'}
          if split_step == 'split_three':
               if en_profit_rate <= -8.22:
                    return api_bidPass(entry_money,en_market,accessKey,secretKey,'split_one','panic_one',user_id)
               else:
                    return {'result':'wait'}




def panic_bid(entry_items,entry_money,accessKey,secretKey,user_id):
     for i in range(0,len(entry_items)):
          en_market = entry_items[i]['market']
          en_profit_rate = entry_items[i]['profit_rate']
          en_profit_rate = float(en_profit_rate)
          # 방어률 -18.0에 도달 했을 때

          user_bid_data = select_recent_bid(user_id,en_market)
          panic_step = user_bid_data['panic_step']

          # 방어률 -18.0에 도달 했을 때, split_two 진행
     
          if panic_step == 'panic_one':
               if en_profit_rate <= -8.70:
                    return api_bidPass(entry_money*2,en_market,accessKey,secretKey,'split_one','panic_two',user_id)
               else:
                    return {'result':'wait'}
          if panic_step == 'panic_two':
               if en_profit_rate <= -9.13:
                    return api_bidPass(entry_money*3,en_market,accessKey,secretKey,'split_one','panic_three',user_id)
               else:
                    return {'result':'wait'}
          if panic_step == 'panic_three':
               if en_profit_rate <= -9.52:
                    return api_bidPass(entry_money*4,en_market,accessKey,secretKey,'split_one','panic_four',user_id)
               else:
                    return {'result':'wait'}
          if panic_step == 'panic_four':
               if en_profit_rate <= -9.88:
                    return {'result':'panic_five'}
               else:
                    return {'result':'wait'}
               

def panic_bid_real(entry_item,entry_money,panic_step,change_rate,accessKey,secretKey,invest_type,user_id):

          if panic_step == 'panic_one':
               if change_rate <= -8.22:
                    return api_bidPass(entry_money,entry_item,accessKey,secretKey,'special','panic_two',invest_type,user_id)
               else:
                    return {'result':'wait'}

          # api_bidPass(price,tickers,accessKey,secretKey,split_step,panic_step,user_id)
          if panic_step == 'panic_two':
               if change_rate <= -8.70:
                    return api_bidPass(entry_money*2,entry_item,accessKey,secretKey,'special','panic_three',invest_type,user_id)
               else:
                    return {'result':'wait'}
          if panic_step == 'panic_three':
               if change_rate <= -9.13:
                    return api_bidPass(entry_money*4,entry_item,accessKey,secretKey,'special','panic_four',invest_type,user_id)
               else:
                    return {'result':'wait'}
          if panic_step == 'panic_four':
               if change_rate <= -9.52:
                    return api_bidPass(entry_money*8,entry_item,accessKey,secretKey,'special','panic_five',invest_type,user_id)
               else:
                    return {'result':'wait'}
          if panic_step == 'panic_five':
               if change_rate <= -9.88:
                    return api_bidPass(entry_money*16,entry_item,accessKey,secretKey,'special','panic_end',invest_type,user_id)
               else:
                    return {'result':'wait'}


def split_panic_bid(entry_items,entry_money,accessKey,secretKey,user_id):
     for i in range(0,len(entry_items)):
          en_market = entry_items[i]['market']
          en_profit_rate = entry_items[i]['profit_rate']
          en_profit_rate = float(en_profit_rate)
          # 방어률 -18.0에 도달 했을 때

          user_bid_data = select_recent_bid(user_id,en_market)
          split_step = user_bid_data['split_step']
          panic_step = user_bid_data['panic_step']

          # 방어률 -18.0에 도달 했을 때, split_two 진행
          if split_step == 'split_one':
               if en_profit_rate <= -18.0:
                    return api_bidPass(entry_money*0.3,en_market,accessKey,secretKey,'split_two',None,user_id)
               else:
                    return {'result':'wait'}
          if split_step == 'split_two':
               if en_profit_rate <= -9.0:
                    return api_bidPass(entry_money*0.4,en_market,accessKey,secretKey,'split_three',None,user_id)
               else:
                    return {'result':'wait'}
          if split_step == 'split_three':
               if en_profit_rate <= -8.22:
                    return api_bidPass(entry_money,en_market,accessKey,secretKey,'split_one','panic_one',user_id)
               else:
                    return {'result':'wait'}
          else:
               if panic_step == 'panic_one':
                    if en_profit_rate <= -8.70:
                         return api_bidPass(entry_money*2,en_market,accessKey,secretKey,'split_one','panic_two',user_id)
                    else:
                         return {'result':'wait'}
               if panic_step == 'panic_two':
                    if en_profit_rate <= -9.13:
                         return api_bidPass(entry_money*3,en_market,accessKey,secretKey,'split_one','panic_three',user_id)
                    else:
                         return {'result':'wait'}
               if panic_step == 'panic_three':
                    if en_profit_rate <= -9.52:
                         return api_bidPass(entry_money*4,en_market,accessKey,secretKey,'split_one','panic_four',user_id)
                    else:
                         return {'result':'wait'}
               if panic_step == 'panic_four':
                    if en_profit_rate <= -9.88:
                              return {'result':'bid_all'}


def split_panic_bid_real(entry_item,traded_price,accessKey,secretKey,profit_rate,split_step,panic_step,invest_type,balance,avg_buy_price,user_id):
     en_profit_rate = float(profit_rate)
     print('en_profit_rate',en_profit_rate)
     time.sleep(3)
     # 방어률 -18.0에 도달 했을 때

     # user_bid_data = select_recent_bid(user_id,entry_item)
     # split_step = user_bid_data['split_step']
     # panic_step = user_bid_data['panic_step']

     # 방어률 -18.0에 도달 했을 때, split_two 진행
     print('split_panic_bid_real method 실행 158')
     if split_step == 'split_one':
          print('split_panic_bid_real method  split_one 진입 160')
          time.sleep(3)
          if en_profit_rate <= -18.0:
               print('split_panic_bid_real method  en_profit_rate <= -18.0 163')
               time.sleep(3)
               return api_bidPass(traded_price,entry_item,accessKey,secretKey,'split_two',None,invest_type,user_id)
          else:
               return {'result':'wait'}
     if split_step == 'split_two':
          if en_profit_rate <= -9.0:
               return api_bidPass(traded_price*(4/3),entry_item,accessKey,secretKey,'split_three',None,invest_type,user_id)
          else:
               return {'result':'wait'}
     if split_step == 'split_three':
          if en_profit_rate <= -7.69:
               return api_bidPass(traded_price*(10/3),entry_item,accessKey,secretKey,'split_to_panic','panic_one',invest_type,user_id)
          else:
               return {'result':'wait'}
     else:
          if panic_step == 'panic_one' and split_step == 'split_to_panic':
               if en_profit_rate <= -8.22:
                    return api_bidPass(traded_price*(20/3),entry_item,accessKey,secretKey,'split_to_panic','panic_two',invest_type,user_id)
               else:
                    return {'result':'wait'}
          if panic_step == 'panic_two' and split_step == 'split_to_panic':
               if en_profit_rate <= -8.70:
                    return api_bidPass(traded_price*(40/3),entry_item,accessKey,secretKey,'split_to_panic','panic_three',invest_type,user_id)
               else:
                    return {'result':'wait'}
          if panic_step == 'panic_three' and split_step == 'split_to_panic':
               if en_profit_rate <= -9.52:
                    return api_bidPass(traded_price*(80/3),entry_item,accessKey,secretKey,'split_to_panic','panic_four',invest_type,user_id)
               else:
                    return {'result':'wait'}
               
          if panic_step == 'panic_four' and split_step == 'split_to_panic':
               if en_profit_rate <= -9.88:
                    return api_bidPass(traded_price*(160/3),entry_item,accessKey,secretKey,'split_to_panic','panic_five',invest_type,user_id)
               else:
                    return {'result':'wait'}
               
          if panic_step == 'panic_five':
               if en_profit_rate <= -9.52 and split_step == 'split_to_panic':
                         trade_price = current_trade_price(entry_item)
                         return  api_askPass(trade_price,balance,entry_item,accessKey,secretKey,avg_buy_price,invest_type,user_id)