import json
from commons.dbConnFetch import *
from operator import itemgetter
from commons.weekDatas import *
import schedule
import time

import psycopg2


DB_NAME = "ybbot"
DB_USER = "ybbot"
DB_PASS = "12341234"
DB_HOST = "15.164.45.203"
DB_PORT = "5432"

conn = psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
cur = conn.cursor()



def week_profit_active_ontime():
     # 전체 사용자 정보 조회
     users = all_usersinfo()
     # 잠시 정렬 -> user : 이한진 중심으로 하기 위해서
     # users = sorted(users,key=itemgetter('id'))

     users_keyList = []
     for i in range(0,len(users)):
          temp = dict()
          temp['user_id'] = users[i]['id']
          # temp['access_key'] = users[i]['access_key']
          # temp['secret_key'] = users[i]['secret_key']
          users_keyList.append(temp)

     test_user_id = users_keyList[0]['user_id']

     datas = sum_today_asks(test_user_id)
     try:
          cur.execute('INSERT INTO week_profit(user_id,trade_count,sum_profit_rate) VALUES (%s,%s,%s)',(test_user_id,datas['trade_count'],datas['sum_profit_rate']))
     except Exception as ex:
          print('save_week_data~~>ex',ex)
          conn.rollback()
     else:
          conn.commit()
     # print('test_user_id',test_user_id)
     return test_user_id


schedule.every().day.at("23:40").do(week_profit_active_ontime)

while(True):

     schedule.run_pending()
