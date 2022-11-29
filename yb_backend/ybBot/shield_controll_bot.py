
import requests
from urllib.parse import urlencode, unquote
from commons.checkStock import view_krw_items
from commons.price import pyupbit_currentPrice
import pandas as pd
import time
from datetime import datetime,timedelta
from pytz import timezone, utc
import psycopg2


DB_NAME = "ybbot"
DB_USER = "ybbot"
DB_PASS = "12341234"
DB_HOST = "15.164.45.203"
DB_PORT = "5432"

conn = psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
cur = conn.cursor()




KST = timezone('Asia/Seoul')




def rsi_upbit(itv, symbol):
     url = "https://api.upbit.com/v1/candles/minutes/"+str(itv)
     querystring = {"market" : symbol, "count" : "200"}
     response = requests.request("GET", url, params=querystring)
     data = response.json()
     df =pd.DataFrame(data)
     df=df.reindex(index=df.index[::-1]).reset_index()
     nrsi=rsi_calc(df, 15).iloc[-1]
     # print("현재" + str(itv) +"분 rsi :" +str(nrsi))

     return nrsi


def rsi_calc(ohlc: pd.DataFrame, period: int = 15):
     ohlc["trad_price"] = ohlc["trade_price"]
     delta = ohlc["trade_price"].diff()
     #     print('delta',delta)
     gains, declines = delta.copy(), delta.copy()
     #     print('gains',gains,'declines',declines)
     gains[gains < 0] = 0
     declines[declines > 0] = 0
     _gain = gains.ewm(com=(period-1), min_periods=period).mean()
     _loss = declines.abs().ewm(com=(period-1), min_periods=period).mean()

     RS = _gain / _loss
     return pd.Series(100-(100/(1+RS)), name="RSI")  


while True:
     # 현재 upbit에 등록된 리스트들 
     ticker_list = view_krw_items()
     # print('ticker_list',ticker_list)
     
     for i in range(0,len(ticker_list)):
          # try:
          #      nrsi = rsi_upbit(1,ticker_list[i])
          # except Exception as ex:
          #      print('ex',ex)
          # else:
          #      print('nrsi', nrsi, ticker_list[i])
          
          # try:
          #      cur.execute('INSERT INTO rsi_rate(market, rsi_value) VALUES(%s,%s)',(ticker_list[i],nrsi))
          # except Exception as ex:
          #      print('INSERT INTO rsi_rate err ',ex)
          #      conn.rollback()
          # else:
          #      conn.commit()
               
          
          now = datetime.now(KST)

          check_time = now.strftime('%Y-%m-%d %H:%M:%S')
          format_ = '%Y-%m-%d %H:%M:%S'
          dt_strptime = datetime.strptime(check_time, format_)
          
          sec5_before = dt_strptime + timedelta(seconds=-5)
          # print('sec5_before',sec5_before)
          # print('now',check_time)
          sec10_before = dt_strptime + timedelta(seconds=-10)
          sec20_before = dt_strptime + timedelta(seconds=-20)
          
          sec5_before = sec5_before.strftime('%Y-%m-%d %H:%M:%S')
          sec10_before = sec10_before.strftime('%Y-%m-%d %H:%M:%S')
          sec20_before = sec20_before.strftime('%Y-%m-%d %H:%M:%S')
          
          try:
               # 현재 체크 지점의 rsi data
               cur.execute('SELECT id,market, rsi_value FROM rsi_rate WHERE update_time <= %s AND market = %s order by id desc limit 1',(check_time,ticker_list[i]))
          except Exception as ex:
               print('SELECT * FROM rsi_rate err ',ex)
               conn.rollback()
          else:
               curent_data = cur.fetchone()
               # print('curent_data id ',curent_data[0])
               
          if curent_data == None:
               pass
          
          elif curent_data[2] <= 45:
               
          
               try:
                    # 5초전 체크 지점의 rsi data
                    cur.execute('SELECT id, market, rsi_value FROM rsi_rate WHERE update_time <= %s AND market = %s order by id desc limit 1',(sec5_before,ticker_list[i]))
               except Exception as ex:
                    print('SELECT * FROM rsi_rate err ',ex)
                    conn.rollback()
               else:
                    sec5_before_data = cur.fetchone()
                    # print(' 5초전 체크 지점의 id',sec5_before_data[0] )
               
               try:
                    # 10초전 체크 지점의 rsi data
                    cur.execute('SELECT id, market, rsi_value FROM rsi_rate WHERE update_time <= %s AND market = %s order by id desc limit 1',(sec10_before,ticker_list[i]))
               except Exception as ex:
                    print('SELECT * FROM rsi_rate err ',ex)
                    conn.rollback()
               else:
                    sec10_before_data = cur.fetchone()
                    # print(' 10초전 체크 지점의 id',sec10_before_data[0] )
               try:
                    # 20초전 체크 지점의 rsi data
                    cur.execute('SELECT id, market, rsi_value FROM rsi_rate WHERE update_time <= %s AND market = %s order by id desc limit 1',(sec20_before,ticker_list[i]))
               except Exception as ex:
                    print('SELECT * FROM rsi_rate err ',ex)
                    conn.rollback()
               else:
                    sec20_before_data = cur.fetchone()
                    
               if sec20_before_data == None:
                    pass
               else:
                    
                    change_rate = (sec20_before_data[2] - curent_data[2]) * 100 / curent_data[2]
                    try:
                         cur.execute("INSERT INTO shield_rate (market,change_rate,type) VALUES(%s,%s,%s)",(ticker_list[i],change_rate,'shield2'))
                    except Exception as ex:
                         print('INSERT INTO shield_rate err ',ex)
                         conn.rollback()
                    else:
                         conn.commit()
                         
               if sec10_before_data == None:
                    pass
               else:
                    
                    change_rate = (sec10_before_data[2] - curent_data[2]) * 100 / curent_data[2]
                    try:
                         cur.execute("INSERT INTO shield_rate (market,change_rate,type) VALUES(%s,%s,%s)",(ticker_list[i],change_rate,'shield1'))
                    except Exception as ex:
                         print('INSERT INTO shield_rate err ',ex)
                         conn.rollback()
                    else:
                         conn.commit()
                         
               if sec5_before_data == None:
                    pass
               else:
                    
                    change_rate = (sec5_before_data[2] - curent_data[2]) * 100 / curent_data[2]
                    try:
                         cur.execute("INSERT INTO shield_rate (market,change_rate,type) VALUES(%s,%s,%s)",(ticker_list[i],change_rate,'shield0'))
                    except Exception as ex:
                         print('INSERT INTO shield_rate err ',ex)
                         conn.rollback()
                    else:
                         conn.commit()
                         
                    
          else:
               pass
          