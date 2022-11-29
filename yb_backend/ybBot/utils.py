import pytz
from time import gmtime, strftime
import datetime


def currenttime():
    tz1 = pytz.timezone("UTC")
    tz2 = pytz.timezone("Asia/Seoul")
    dt = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    dt = datetime.datetime.strptime(dt,"%Y-%m-%d %H:%M:%S")
    dt = tz1.localize(dt)
    dt = dt.astimezone(tz2)
    dt = dt.strftime("%Y-%m-%d %H:%M:%S")
    return dt





# # 병철님 의사코드

# def order223(APIkey, SecretKey, Amount, side):
#      r = (url + "/orderbook")
#      msg = ""
#      if side == "buy":
#           lowest_bid_price = ewfewfwef
#           r = (url + "/buy?parms=  apikey, secret key, amount, lowest_bid_price")
#           msg = r.json()
#      else:
#           highest_ask_price = ewfewfwef
#           r = requests.get(url + "/sell?parms=  apikey, secret key, amount, highest_ask_price")
#           msg = r.json()

#      return msg