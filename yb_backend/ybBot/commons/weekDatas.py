from .dbConnFetch import dbConn_no_cur

conn = dbConn_no_cur()
cur = conn.cursor()


def select_ask_data(user_id):
     try:
          cur.execute("SELECT volume,price,avg_bid_price FROM transactions WHERE user_id=%s AND side ='ask' AND work_time >= NOW() - INTERVAL '24 HOURS' ",(user_id,))
     except Exception as ex:
          print('select_ask_data',ex)
     else:
          temp = cur.fetchall()
     
     return temp

def sum_today_asks(user_id):
     today_ask_list = select_ask_data(user_id)
     sum_profit_rate = float()
     for i in range(0,len(today_ask_list)):
          volume = today_ask_list[i][0]
          price = today_ask_list[i][1]
          avg_bid_price = today_ask_list[i][2]
          volume = float(volume)
          price = float(price)
          avg_bid_price = float(avg_bid_price)
          dt = price - avg_bid_price
          single_profit_rate = dt / avg_bid_price
          sum_profit_rate = sum_profit_rate + single_profit_rate
     
          
     return {'sum_profit_rate':sum_profit_rate,'trade_count':len(today_ask_list)}

# def save_week_data(user_id):
#      print('35 실행 확인')
#      datas = sum_today_asks(user_id)
#      print('datas 36',datas)
#      try:
#           cur.execute('INSERT INTO week_profit(user_id,trade_count,sum_profit_rate) VALUES (%s,%s,%s)',(user_id,datas['trade_count'],datas['sum_profit_rate']))
#      except Exception as ex:
#           print('save_week_data~~>ex',ex)
#           conn.rollback()
#      else:
#           conn.commit()
#           pass
#      return None