from tempfile import TemporaryFile, tempdir
from flask import request,redirect,url_for
from ..dbConn import dbConn
import json
import pyupbit as ub

conn = dbConn()
cur = conn.cursor()

def keyupdate(apikey,secretkey,email):

     upbit = ub.Upbit(access=apikey, secret=secretkey)
     my_balance = upbit.get_balances()
     if type(my_balance) == dict:
          return redirect(url_for('view_mypage',errMsg='upbit에 등록된 API KEY가 아닙니다.',error='error'))
     else:
          try: 
               cur.execute('UPDATE users SET apikey=%s,secretkey=%s WHERE email=%s',(apikey,secretkey,email)) 
          except Exception as ex:
               print('ex',ex)
               redirect('/mypage')
          else:
               conn.commit()
               pass
               return redirect('/mypage')


def accessKey_select(user_id):
     # temp_dict = dict()
     # temp_tuple =tuple()
     try:
          cur.execute('SELECT apikey FROM users WHERE id=%s',(user_id,))
     except Exception as ex:
          print('ex',ex)
          conn.rollback()
     else:
          temp_tuple = cur.fetchone()
          accessKey = temp_tuple[0]
          # secretkey = temp_tuple[1]
          # temp_dict['apikey'] = apikey
          # # temp_dict['secretkey'] = secretkey
          # print('temp_dict ---', temp_dict)
          pass

     return {'accessKey': accessKey}