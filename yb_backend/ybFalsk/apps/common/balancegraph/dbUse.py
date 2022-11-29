from ..dbConn import dbConn
from time import strftime

conn = dbConn()
cur = conn.cursor()

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

def select_ask_data(user_id):
     
     user_id = 1
     try:
          cur.execute("SELECT * FROM transactions WHERE user_id=%s AND side ='ask'",(user_id,))
     except Exception as ex:
          print('select_ask_data',ex)
     else:
          temp = cur.fetchall()
          
     return temp