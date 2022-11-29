from .dbConn import *
from passlib.hash import sha256_crypt
import json
import jwt


conn = dbConn()
cur = conn.cursor()

key = "ybbot_secert"

def method_admin_signup(data):
     login_id = data['loginId']
     password = data['password']
     password = sha256_crypt.encrypt(password)
     wallet = data['wallet']
     privatekey = data['privatekey']
     try:
          cur.execute("INSERT INTO admins(login_id, password, wallet, privatekey) VALUES(%s,%s,%s,%s)",(login_id, password, wallet, privatekey))
     except Exception as ex:
          print('method_admin_signup err', ex)
          conn.rollback()
     else:
          conn.commit()
          return json.dumps({'result':'success'}), 200, {'Content-Type':'application/json'}



def method_notice_insert(data):
     notice_type = data['notice_type']
     title = data['title']
     description = data['description']
     try:
          cur.execute("INSERT INTO notice(notice_type,title,description) VALUES(%s,%s,%s)",(notice_type,title,description))
     except Exception as ex:
          # print('ex',ex)
          conn.rollback()
     else:
          conn.commit()
          
     return json.dumps({'result':'success'}), 200, {'Content-Type':'application/json'}


def method_question_insert(data):
     notice_type = data['q_type']
     title = data['title']
     description = data['description']
     try:
          cur.execute("INSERT INTO question(q_type,title,description) VALUES(%s,%s,%s)",(notice_type,title,description))
     except Exception as ex:
          # print('ex',ex)
          conn.rollback()
     else:
          conn.commit()
          
     return json.dumps({'result':'success'}), 200, {'Content-Type':'application/json'}


def method_ybPoint_refund(data):
     
     token = data["sessionToken"]
     decoded = jwt.decode(token, key, algorithms="HS256")
     id = decoded["id"]
     amount = data["amount"]
     user_id = data["user_id"]
     amount = float(amount)
     # print('id',id,amount,user_id,amount)
     
     try:
          cur.execute("SELECT SUM(provided_p), SUM(used_p) FROM yb_point WHERE user_id = %s",(user_id,))
     except Exception as ex:
          print('method_user_point_voucher_info err', ex)
     else:
          temp = cur.fetchone()
          provided_p = temp[0]
          used_p = temp[1]
          left_point = provided_p + used_p
          left_point = float(left_point)
          
     if left_point < amount:
          return json.dumps({'errMsg':'보유한 포인트가 부족합니다.'}), 400, {'Content-Type':'application/json'}
     
     if id == 1:
          
          try:
               cur.execute("INSERT INTO yb_point(user_id,used_p) VALUES(%s,%s)",(user_id,-amount))
          except Exception as ex:
               print('ex',ex)
               conn.rollback()
          else:
               conn.commit()
               
          return json.dumps({'result':'success'}), 200, {'Content-Type':'application/json'}
     else:
          return json.dumps({'errMsg':'success'}), 400, {'Content-Type':'application/json'}



def method_ybPoint_provide(data):
     
     token = data["sessionToken"]
     decoded = jwt.decode(token, key, algorithms="HS256")
     id = decoded["id"]
     amount = data["amount"]
     user_id = data["user_id"]
     amount = float(amount)
     # print('id',id,amount,user_id,amount)
     
     try:
          cur.execute("SELECT SUM(provided_p), SUM(used_p) FROM yb_point WHERE user_id = %s",(user_id,))
     except Exception as ex:
          print('method_user_point_voucher_info err', ex)
     else:
          temp = cur.fetchone()
          provided_p = temp[0]
          used_p = temp[1]
          left_point = provided_p + used_p
          left_point = float(left_point)
          
     # if left_point < amount:
     #      return json.dumps({'errMsg':'보유한 포인트가 부족합니다.'}), 400, {'Content-Type':'application/json'}
     
     if id == 1:
          
          try:
               cur.execute("INSERT INTO yb_point(user_id,provided_p) VALUES(%s,%s)",(user_id,amount))
          except Exception as ex:
               print('ex',ex)
               conn.rollback()
          else:
               conn.commit()
               
          return json.dumps({'result':'success'}), 200, {'Content-Type':'application/json'}
     else:
          return json.dumps({'errMsg':'success'}), 400, {'Content-Type':'application/json'}
          