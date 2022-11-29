import pytz
from time import gmtime, strftime,sleep
import datetime 
import psycopg2


DB_NAME = "ybbot"
DB_USER = "ybbot"
DB_PASS = "12341234"
DB_HOST = "15.164.45.203"
DB_PORT = "5432"

conn = psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
cur = conn.cursor()

def currenttime():
    tz1 = pytz.timezone("UTC")
    tz2 = pytz.timezone("Asia/Seoul")
    dt = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    dt = datetime.datetime.strptime(dt,"%Y-%m-%d %H:%M:%S")
    dt = tz1.localize(dt)
    dt = dt.astimezone(tz2)
    dt = dt.strftime("%Y-%m-%d %H:%M:%S")
    return dt


def dbConn():
     conn = psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
     cur = conn.cursor()
     return cur

def dbConn_no_cur():
     dbconn = psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
     return dbconn

def all_usersinfo():
     try:
          cur.execute("SELECT * FROM users WHERE type = 'user' AND registered = 'True' AND start_active = 'False' ")
     except Exception as ex:
          print('usersinfo',ex)
     else:
          users = cur.fetchall()
          
     resultList = []
     for k in range(0, len(users)):
          userDict = dict()
          userDict['id'] = users[k][0]
          userDict['username'] = users[k][1]
          # userDict['password'] = users[k][2]
          userDict['phone'] = users[k][2]
          userDict['email'] = users[k][4]
          userDict['access_key'] = users[k][6]
          userDict['secret_key'] = users[k][7]
          userDict['swing_cockpit'] = users[k][14]
          userDict['swing_point'] = users[k][15]
          userDict['panic_cell'] = users[k][16]
          userDict['seed_money'] = users[k][17]
          userDict['entry_money'] = users[k][18]

          if users[k][4] == None:
               pass
               # print('email 등록안된 사람 처리')
          else: 
               resultList.append(userDict)
               
     return resultList

def usersinfos():
     try:
          cur.execute("SELECT id,invest_type,apikey,secretkey,panic_cell,seed_money,entry_money FROM users WHERE type = 'user' AND registered = 'True' AND start_active = 'True'")
     except Exception as ex:
          print('usersinfo',ex)
     else:
          users = cur.fetchall()

     resultList = []
     for k in range(0, len(users)):
          userDict = dict()
          userDict['id'] = users[k][0]
          userDict['invest_type'] = users[k][1]
          userDict['apikey'] = users[k][2]
          userDict['secretkey'] = users[k][3]
          userDict['panic_cell'] = users[k][4]
          userDict['seed_money'] = users[k][5]
          userDict['entry_money'] = users[k][6]

          if users[k][2] == None:
               pass
               # print('email 등록안된 사람 처리')
          else: 
               resultList.append(userDict)
               
     return resultList

def lookup_userKey():
     try:
          cur.execute("SELECT * FROM users WHERE type = 'user' AND registered = 'true' AND start_active = 'true'")
     except Exception as ex:
          print('usersinfo',ex)
     else:
          users = cur.fetchall()
          
     resultList = []
     for k in range(0, len(users)):
          userDict = dict()
          userDict['id'] = users[k][0]
          # userDict['username'] = users[k][1]
          # # userDict['password'] = users[k][2]
          # userDict['phone'] = users[k][2]
          # userDict['email'] = users[k][4]
          userDict['access_key'] = users[k][6]
          userDict['secret_key'] = users[k][7]
          # userDict['swing_cockpit'] = users[k][14]
          # userDict['swing_point'] = users[k][15]
          # userDict['panic_cell'] = users[k][16]
          # userDict['seed_money'] = users[k][17]
          # userDict['entry_money'] = users[k][18]
          resultList.append(userDict)
               
     return resultList


def cur_price_insert(market,trade_price,user_id):
     
     cur_time = currenttime()

     try:
          cur.execute('INSERT INTO curprice(market,user_id,trade_price,cur_time) VALUES(%s,%s,%s,%s)',(market,user_id,trade_price,cur_time))
     except Exception as ex:
          return {'errMsg':ex}, 400
     else:
          conn.commit()
          pass
          # return {'market':market,'user_id':user_id,'trade_price':trade_price,'cur_time':cur_time}
          return {'result':'success'} ,200

def on_rate_cal(balance_list):
     cur_priceList = []
     for i in range(0,len(balance_list)):
          market = balance_list[i]['market']
          # print('testssts',market,'i--->',i)
          try:
               cur.execute('select * from curPrice WHERE market =%s ORDER by cur_time limit 2;',(market,))
          except Exception as ex:
               return {'errMsg':'failed'}, 400
          else:
               temp = cur.fetchall()

          inital_dict = dict()
          change_dict = dict()
          for k in range(0,len(temp)):
               temp_dict = dict()
               if k == 0:
                    inital_dict['market'] = temp[k][1]
                    inital_dict['inital_val'] = temp[k][3]
               else:
                    change_dict['market'] = temp[k][1]
                    change_dict['change_val'] = temp[k][3]

     
          inital_val = float(inital_dict['inital_val'])
          change_val = float(change_dict['change_val'])


          variation = change_val - inital_val
          rate = variation/inital_val
          temp_dict['market'] = market
          temp_dict['rate'] = rate * 100
          cur_priceList.append(temp_dict)

          return cur_priceList

def save_currency(seed_money,entry_money,user_id):
     if user_id !=1:
          try:
               cur.execute('UPDATE users SET seed_money = %s, entry_money = %s WHERE id = %s',(seed_money,entry_money,user_id,))
          except Exception as ex:
               print('save_currency ex',ex)
               conn.rollback()
          else:
               conn.commit()
               return 'success'
     else:
          try:
               cur.execute('UPDATE users SET seed_money = %s, entry_money = %s WHERE id = %s',(seed_money,5500,user_id,))
          except Exception as ex:
               print('save_currency ex',ex)
               conn.rollback()
          else:
               conn.commit()
               return 'success'

     return {'result':'update_success'}


def select_recent_bid(user_id,market):
     # print('user_id',user_id)
     # print('market',market)
     # sleep(3)
     try:
          cur.execute("select market, side, price, MAX(work_time),ord_type, split_step, panic_step, price from transactions where user_id = %s and market= %s and side = 'bid' and ord_type = 'price' GROUP BY market,side,price,ord_type,split_step,panic_step order by MAX(work_time) desc",(user_id,market))
     except Exception as ex:
          print('select_recent_bid err',ex)
          conn.rollback()
     else:
          temp = cur.fetchone()
          # print('temp 207', temp)
     
     if temp != None:
          temp_dict = dict()
          temp_dict['market'] = temp[0]
          temp_dict['side'] = temp[1]
          temp_dict['en_price'] = temp[2]
          temp_dict['update_time'] = temp[3].strftime('%Y-%m-%d %H:%M:%S')
          temp_dict['ord_type'] = temp[4]
          temp_dict['split_step'] = temp[5]
          temp_dict['panic_step'] = temp[6]
          temp_dict['traded_price'] = temp[7]
          return temp_dict
     else:
          temp_dict = dict()
          return temp_dict
     

def select_erc_tokens():
     try:
          cur.execute('select * from erc_tokentxns ORDER BY erc_id desc')
     except Exception as ex:

          conn.rollback()
     else:
          temp_list = cur.fetchall()
     
     return temp_list



def save_day_quotation(market,trade_price,change_rate):
     try:
          cur.execute('INSERT INTO day_quotation(market,trade_price,change_rate) VALUES(%s,%s,%s)',(market,trade_price,change_rate))
     except Exception as ex:
          conn.rollback()
     else:
          conn.commit()
     
          return {'result':f'success {market}'}

def select_day_quotation():
     try:
          cur.execute('SELECT market, trade_price, change_rate, update_time FROM day_quotation WHERE (market,update_time) IN (select market,max(update_time) FROM day_quotation GROUP BY market) ORDER BY update_time DESC')
     except Exception as ex:
          conn.rollback()
     else:
          quotationList = cur.fetchall()
     return quotationList

# .strftime("%Y-%m-%d %H:%M:%S")
def rate_datas_default():
     rate_list = list()
     try:
          cur.execute("SELECT market, change_rate, update_time,type FROM rate WHERE (market,update_time) IN (select market,max(update_time) FROM rate WHERE type = 'attack0' GROUP BY market) ORDER BY update_time DESC")
          # cur.execute("SELECT market, change_rate, update_time,type FROM rate WHERE (market,update_time) IN (select market,max(update_time) FROM rate WHERE type = 'attack0' AND update_time >= NOW() - INTERVAL '10 second' GROUP BY market) ORDER BY update_time DESC")
     except Exception as ex:
          print('rate_datas err',ex)
     else:
          rate_list = cur.fetchall()
          new_temp_list = list()
          for i in range(0,len(rate_list)):
               temp_dict = dict()
               temp_dict["market"] = rate_list[i][0]
               temp_dict['change_rate'] = rate_list[i][1]
               temp_dict['update_time'] = rate_list[i][2].strftime("%Y-%m-%d %H:%M:%S")
               temp_dict['invest_type'] = rate_list[i][3]
               new_temp_list.append(temp_dict)
               
          return new_temp_list
     
     
def rate_datas_attack1():
     rate_list = list()
     try:
          cur.execute("SELECT market, change_rate, update_time,type FROM rate WHERE (market,update_time) IN (select market,max(update_time) FROM rate WHERE type = 'attack1' AND update_time >= NOW() - INTERVAL '10 seconds' GROUP BY market) ORDER BY update_time DESC")
          # cur.execute("SELECT market, change_rate, update_time,type FROM rate WHERE (market,update_time) IN (select market,max(update_time) FROM rate WHERE type = 'attack1' GROUP BY market) ORDER BY update_time DESC")
     except Exception as ex:
          print('rate_datas err',ex)
     else:
          rate_list = cur.fetchall()
          new_temp_list = list()
          for i in range(0,len(rate_list)):
               temp_dict = dict()
               temp_dict["market"] = rate_list[i][0]
               temp_dict['change_rate'] = rate_list[i][1]
               temp_dict['update_time'] = rate_list[i][2].strftime("%Y-%m-%d %H:%M:%S")
               temp_dict['invest_type'] = rate_list[i][3]
               new_temp_list.append(temp_dict)
               
          return new_temp_list
     
def rate_datas_attack2():
     rate_list = list()
     try:
          cur.execute("SELECT market, change_rate, update_time,type FROM rate WHERE (market,update_time) IN (select market,max(update_time) FROM rate WHERE type = 'attack2' AND update_time >= NOW() - INTERVAL '10 seconds' GROUP BY market) ORDER BY update_time DESC")
     except Exception as ex:
          print('rate_datas err',ex)
     else:
          rate_list = cur.fetchall()
          new_temp_list = list()
          for i in range(0,len(rate_list)):
               temp_dict = dict()
               temp_dict["market"] = rate_list[i][0]
               temp_dict['change_rate'] = rate_list[i][1]
               temp_dict['update_time'] = rate_list[i][2].strftime("%Y-%m-%d %H:%M:%S")
               temp_dict['invest_type'] = rate_list[i][3]
               new_temp_list.append(temp_dict)
               
          return new_temp_list
     


def rate_datas_special_increase():
     rate_list = list()
     try:
          cur.execute("SELECT market, change_rate, update_time,type FROM rate WHERE (market,update_time) IN (select market,max(update_time) FROM rate WHERE type = 'special' AND update_time >= NOW() - INTERVAL '10 second' GROUP BY market) ORDER BY update_time DESC")
     except Exception as ex:
          print('rate_datas_special_increase err',ex)
     else:
          rate_list = cur.fetchall()
          new_temp_list = list()
          for i in range(0,len(rate_list)):
               temp_dict = dict()
               temp_dict["market"] = rate_list[i][0]
               temp_dict['change_rate'] = rate_list[i][1]
               temp_dict['update_time'] = rate_list[i][2].strftime("%Y-%m-%d %H:%M:%S")
               temp_dict['invest_type'] = rate_list[i][3]
               new_temp_list.append(temp_dict)
               
          return new_temp_list
     


def rate_datas_special_decrease():
     rate_list = list()
     try:
          cur.execute("SELECT market, change_rate, update_time,type FROM rate WHERE (market,update_time) IN (select market,max(update_time) FROM rate WHERE type = 'decrease' AND update_time >= NOW() - INTERVAL '10 second' GROUP BY market) ORDER BY update_time DESC")
     except Exception as ex:
          print('rate_datas_special_increase err',ex)
     else:
          rate_list = cur.fetchall()
          new_temp_list = list()
          for i in range(0,len(rate_list)):
               temp_dict = dict()
               temp_dict["market"] = rate_list[i][0]
               temp_dict['change_rate'] = rate_list[i][1]
               temp_dict['update_time'] = rate_list[i][2].strftime("%Y-%m-%d %H:%M:%S")
               temp_dict['invest_type'] = rate_list[i][3]
               new_temp_list.append(temp_dict)
               
          return new_temp_list
     
     
     
     
def market_profit_rate_search(user_id, market):
     try:
          cur.execute("SELECT profit_rate FROM balances WHERE user_id = %s AND market = %s",(user_id,market))
     except Exception as ex:
          print('market_profit_rate_search err', ex)
          conn.rollback()
     else:
          profit_rate = cur.fetchone()[0]
     return profit_rate
     
     
     
def rate_datas_shield0():
     rate_list = list()
     try:
          cur.execute("SELECT market, change_rate, update_time, type FROM shield_rate WHERE (market,update_time) IN (select market,max(update_time) FROM shield_rate WHERE type = 'shield0' AND update_time >= NOW() - INTERVAL '10 seconds' GROUP BY market) ORDER BY update_time DESC")
          # cur.execute("SELECT market, change_rate, update_time,type FROM rate WHERE (market,update_time) IN (select market,max(update_time) FROM rate WHERE type = 'attack1' GROUP BY market) ORDER BY update_time DESC")
     except Exception as ex:
          print('rate_datas err',ex)
     else:
          rate_list = cur.fetchall()
          new_temp_list = list()
          for i in range(0,len(rate_list)):
               temp_dict = dict()
               temp_dict["market"] = rate_list[i][0]
               temp_dict['change_rate'] = rate_list[i][1]
               temp_dict['update_time'] = rate_list[i][2].strftime("%Y-%m-%d %H:%M:%S")
               temp_dict['invest_type'] = rate_list[i][3]
               new_temp_list.append(temp_dict)
               
          return new_temp_list
     

     
def rate_datas_shield1():
     rate_list = list()
     try:
          cur.execute("SELECT market, change_rate, update_time, type FROM shield_rate WHERE (market,update_time) IN (select market,max(update_time) FROM shield_rate WHERE type = 'shield1' AND update_time >= NOW() - INTERVAL '10 seconds' GROUP BY market) ORDER BY update_time DESC")
          # cur.execute("SELECT market, change_rate, update_time,type FROM rate WHERE (market,update_time) IN (select market,max(update_time) FROM rate WHERE type = 'attack1' GROUP BY market) ORDER BY update_time DESC")
     except Exception as ex:
          print('rate_datas err',ex)
     else:
          rate_list = cur.fetchall()
          new_temp_list = list()
          for i in range(0,len(rate_list)):
               temp_dict = dict()
               temp_dict["market"] = rate_list[i][0]
               temp_dict['change_rate'] = rate_list[i][1]
               temp_dict['update_time'] = rate_list[i][2].strftime("%Y-%m-%d %H:%M:%S")
               temp_dict['invest_type'] = rate_list[i][3]
               new_temp_list.append(temp_dict)
               
          return new_temp_list
     
     
     
def rate_datas_shield2():
     rate_list = list()
     try:
          cur.execute("SELECT market, change_rate, update_time, type FROM shield_rate WHERE (market,update_time) IN (select market,max(update_time) FROM shield_rate WHERE type = 'shield2' AND update_time >= NOW() - INTERVAL '10 seconds' GROUP BY market) ORDER BY update_time DESC")
          # cur.execute("SELECT market, change_rate, update_time,type FROM rate WHERE (market,update_time) IN (select market,max(update_time) FROM rate WHERE type = 'attack1' GROUP BY market) ORDER BY update_time DESC")
     except Exception as ex:
          print('rate_datas err',ex)
     else:
          rate_list = cur.fetchall()
          new_temp_list = list()
          for i in range(0,len(rate_list)):
               temp_dict = dict()
               temp_dict["market"] = rate_list[i][0]
               temp_dict['change_rate'] = rate_list[i][1]
               temp_dict['update_time'] = rate_list[i][2].strftime("%Y-%m-%d %H:%M:%S")
               temp_dict['invest_type'] = rate_list[i][3]
               new_temp_list.append(temp_dict)
               
          return new_temp_list    