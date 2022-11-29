from time import sleep,localtime,gmtime, strftime
import datetime
import requests
import json
from .dbConnFetch import cur_price_insert
import time
import pyupbit
import pytz
import asyncio


# import asyncio

def currenttime():
    tz1 = pytz.timezone("UTC")
    tz2 = pytz.timezone("Asia/Seoul")
    dt = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    dt = datetime.datetime.strptime(dt,"%Y-%m-%d %H:%M:%S")
    dt = tz1.localize(dt)
    dt = dt.astimezone(tz2)
    dt = dt.strftime("%Y-%m-%d %H:%M:%S")
    return dt





# def on_current_price(balance_list,user_id):

#           for i in range(0,len(balance_list)):
#                for count in range(0,2):
#                     print('count',count)
#                     print('tm_sec:',localtime(time.time()).tm_sec)
#                     # print('i',i,'balance_list',balance_list)
          
#                     url = f"https://api.upbit.com/v1/ticker?markets={balance_list[i]['market']}"

#                     headers = {"Accept": "application/json"}

#                     response = requests.get(url, headers=headers)

          
#                     current_price_info = response.json()[0]
#                     market = current_price_info['market']
#                     trade_price = current_price_info['trade_price']

#                     try:
#                          cur_price_insert(market,trade_price,user_id)
#                          time.sleep(3)
#                     except Exception as ex:
#                          return {'errMsg':ex}, 400
                    
                    
#           return {'result':'success'}, 200


def pyupbit_currentPrice(ticker):
     price = pyupbit.get_current_price(ticker)
     return price

async def sudden_sale_rate(ticker):
     inital_price = pyupbit_currentPrice(ticker)
     await asyncio.sleep(3)
     change_price = pyupbit_currentPrice(ticker)
     # await asyncio.sleep(3)
     inital_price = float(inital_price)
     change_price = float(change_price)
     dt = change_price - inital_price
     rate = dt / inital_price
     rate = rate * 100


     return rate

async def currentPrice(ticker):
     inital_price = pyupbit_currentPrice(ticker)
     await asyncio.sleep(4)
     return inital_price


# async def async_current_price(balance_list):

#      for i in range(0,len(balance_list)):
#           temp = dict()
#           url = f"https://api.upbit.com/v1/ticker?markets={balance_list[i]['market']}"

#           headers = {"Accept": "application/json"}

#           response = requests.get(url, headers=headers)

#           print('trsgtew',response.json())

#           current_price_info = response.json()[0]
#           market = current_price_info['market']
#           trade_price = current_price_info['trade_price']

#      await asyncio.sleep(1.0)

#      return {'market':market,'trade_price':trade_price}

# async def async_current_price_save(user_id):
#      data = await async_current_price(user_id)

#      cur_price_insert(data['market'],data['trade_price'],user_id)

#      return {'result':'success'}, 200



