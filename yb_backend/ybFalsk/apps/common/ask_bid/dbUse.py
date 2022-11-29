from ..dbConn import dbConn
import json
conn = dbConn()
cur = conn.cursor()

def order_save(user_id,market,side,volume,price,uuid,ord_type,avg_bid_price,split_step,panic_step):
     try:
          cur.execute('INSERT INTO transactions(trans_id,user_id,market,side,volume,price,uuid,ord_type,avg_bid_price,split_step,panic_step) VALUES((SELECT MAX(trans_id)+1 FROM transactions),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(user_id,market,side,volume,price,uuid,ord_type,avg_bid_price,split_step,panic_step))
     except Exception as ex:
          print('ex',ex)
          conn.rollback()
     else:
          conn.commit()
          pass
     return json.dumps({'result':'order_save'}), 200, {'Content-Type':'application/json'}



def select_uuids_market(user_id):

     try:
          cur.execute('SELECT market,uuid FROM transactions WHERE user_id = %s AND active = True',(user_id,))
     except Exception as ex:
          print('ex',ex)
     else:
          temp = cur.fetchall()
          pass
     
     eventList = []
     for i in range(0,len(temp)):
          tempdict = dict()
          tempdict['market'] = temp[i][0]
          tempdict['uuid'] = temp[i][1]
          eventList.append(tempdict)

     return eventList

def select_orderMarket(user_id):

     try:
          cur.execute('SELECT market FROM transactions WHERE user_id = %s AND active = True',(user_id,))
     except Exception as ex:
          print('ex',ex)
     else:
          temp = cur.fetchall()
          pass
     
     eventList = []
     for i in range(0,len(temp)):
          eventList.append(temp[i][0])

     return eventList    

def tickers(user_id):
     marketList = select_orderMarket(user_id)
     return marketList