from flask_login import current_user
import requests
import json

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

# def order(Volume, Price, Side):
def pass_ask(volume,trade_price,ticker,accessKey,secretKey,avg_bid_price,auto_set,user_id):

     temp_dict = {
          'volume':volume,
          'trade_price':trade_price,
          'ticker':ticker,
          'accessKey':accessKey,
          'secretKey':secretKey,
          'avg_bid_price':avg_bid_price,
          'auto_set':auto_set,
          'user_id':user_id
          
          }
     try:
          req = requests.post('http://ybELB-1534994838.ap-northeast-2.elb.amazonaws.com/asksend',data=json.dumps(temp_dict), headers=headers)
          # req = requests.post('http://127.0.0.1:5000/asksend',data=json.dumps(temp_dict), headers=headers)
     except Exception as ex:
          print('ex',ex)
          return json.dumps({'errMsg':'failed'}), 400, {'Content-Type':'application/json'}
     else:

          # if req.json()['error']:
          #      return json.dumps({'errMsg':'failed'}), 400, {'Content-Tpye':'application/json'}
          return json.dumps({'result':'seuccess'}), 200, {'Content-Type':'application/json'}


def  pass_bid(accessKey,secretKey,price,tickers,split_step,panic_step,user_id,auto_set):

     temp_dict = {
          'accessKey':accessKey,
          'secretKey':secretKey,
          'price':price,
          'tickers':tickers,
          'split_step':split_step,
          'panic_step':panic_step,
          'auto_set':auto_set,
          'user_id':user_id,
          }
     try:
          # req = requests.post('http://127.0.0.1:5000/bidsend',data=json.dumps(temp_dict),headers=headers)
          req = requests.post('http://ybELB-1534994838.ap-northeast-2.elb.amazonaws.com/bidsend',data=json.dumps(temp_dict),headers=headers)

     except Exception as ex:
          print('ex pass_bid',ex)
          return json.dumps({'errMsg':'failed'}), 400, {'Content-Type':'application/json'}
     else:

          # if req.json()['error']:
          #      return json.dumps({'errMsg':'failed'}), 400, {'Content-Tpye':'application/json'}
          return json.dumps(req.json()), 200, {'Content-Type':'application/json'}

