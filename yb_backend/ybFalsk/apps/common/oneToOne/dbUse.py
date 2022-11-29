from ybBot.commons.requests import current_trade_price
from flask import redirect,url_for
from ..dbConn import dbConn
import json

conn = dbConn()
cur = conn.cursor()


def method_one_to_one_insert(username,email,phone,title,questions):
     try:
          cur.execute("INSERT INTO onetoone(username,email,phone,title,questions) VALUES(%s,%s,%s,%s,%s)",(username,email,phone,title,questions))
     except Exception as ex:
          print('method_one_to_one_insert err ', ex)
          conn.rollback()
     else:
          conn.commit()
          
     return redirect('/main')
     