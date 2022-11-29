from ast import expr_context
from glob import escape
from .dbConn import *
from passlib.hash import sha256_crypt
import json
import jwt


conn = dbConn()
cur = conn.cursor()

key = "ybbot_secert"

def method_notice_list():
     try:
          cur.execute("SELECT notice_id, notice_type, title, description, notice_time FROM notice WHERE active = true")
     except Exception as ex:
          # print('method_user_list',ex)
          return json.dumps({'result':ex}) , 400, {'Content-Type':'application/json'}
     else:
          notice_list = cur.fetchall()
          
          new_notice_list = list()
          for i in range(0,len(notice_list)):
               notice_dict = dict()
               notice_dict['id'] = notice_list[i][0]
               notice_dict['type'] = notice_list[i][1]
               notice_dict['title'] = notice_list[i][2]
               notice_dict['description'] = notice_list[i][3]
               notice_dict['notice_time'] = notice_list[i][4].strftime("%Y-%m-%d %H:%M:%S")
               new_notice_list.append(notice_dict)
               
     return json.dumps({'result':new_notice_list}), 200, {'Content-Type':'application/json'}


def method_user_list():
     try:
          cur.execute("SELECT id, username, phone, email, apikey, start_active FROM users WHERE registered = true ORDER BY id DESC")
     except Exception as ex:
          # print('method_user_list',ex)
          return json.dumps({'errMsg':ex}) , 400, {'Content-Type':'application/json'}
     else:
          user_list = cur.fetchall()
          
          new_user_list = list()
          for i in range(0,len(user_list)):
               notice_dict = dict()
               notice_dict['id'] = user_list[i][0]
               notice_dict['username'] = user_list[i][1]
               notice_dict['phone'] = user_list[i][2]
               notice_dict['email'] = user_list[i][3]
               notice_dict['apikey'] = user_list[i][4]
               notice_dict['start_active'] = user_list[i][5]
               new_user_list.append(notice_dict)
               
     return json.dumps({'result':new_user_list}), 200, {'Content-Type':'application/json'}

# 
def adminLogin(loginId,password):

     user_infos = list()
     try:
          cur.execute('SELECT id, login_id, wallet, password FROM admins WHERE login_id = %s',(loginId,))
     except Exception as ex:
          # print('method_nomalLogin_select_err',ex)
          return json.dumps({'errMsg',ex}), 400, {'Content-Type':'application/json'}
     else:
          user_infos = cur.fetchone()
          id = user_infos[0]
          login_id = user_infos[1]
          wallet = user_infos[2]
          curr_password = user_infos[3]

     if sha256_crypt.verify(password,curr_password):
          encoded = jwt.encode({"id": id, "login_id": login_id,"wallet_addr":wallet}, key, algorithm="HS256")
          return json.dumps({"sessionToken": encoded ,"type": "admin","id":id,"login_id":login_id,"wallet":wallet}), 200, {'ContentType':'application/json'}
     else:
          return json.dumps({'errMsg':'비밀번호가 일치하지 않습니다.'}), 400, {'Content-Type':'application/json'}
     
     
# def method_select_transcation(data):
#      user_id = data['id']
#      try:
#           cur.execute("SELECT trans_id, market, side, volume, price, work_time FROM transactions WHERE user_id = %s ORDER BY trans_id DESC",(user_id,))
#      except Exception as ex:
#           print('method_select_transcation err ', ex)
#           return json.dumps({'errMsg':ex}), 400, {'Content-Type':'application/json'}
#      else:
#           transaction_list = cur.fetchall()
          
#           new_transaction_list = list()
#           for i in range(0,len(transaction_list)):
#                transaction_dict = dict()
#                transaction_dict['id'] = transaction_list[i][0]
#                transaction_dict['market'] = transaction_list[i][1]
#                transaction_dict['side'] = transaction_list[i][2]
#                transaction_dict['volume'] = transaction_list[i][3]
#                transaction_dict['price'] = transaction_list[i][4]
#                transaction_dict['work_time'] = transaction_list[i][5].strftime("%Y-%m-%d %H:%M:%S")
#                new_transaction_list.append(transaction_dict)
               
#      return json.dumps({'result':new_transaction_list}), 200, {'Content-Type':'application/json'}


def method_select_question():

     try:
          cur.execute("SELECT q_id, q_type, title, description FROM question WHERE active = true")
     except Exception as ex:
          print('method_select_question err ', ex)
          return json.dumps({'errMsg':ex}), 400, {'Content-Type':'application/json'}
     else:
          question_list = cur.fetchall()
          # print('question_list',question_list)
          
          new_question_list = list()
          for i in range(0,len(question_list)):
               question_dict = dict()
               question_dict['id'] = question_list[i][0]
               question_dict['q_type'] = question_list[i][1]
               question_dict['title'] = question_list[i][2]
               question_dict['description'] = question_list[i][3]
               new_question_list.append(question_dict)
               
     return json.dumps({'result':new_question_list}), 200, {'Content-Type':'application/json'}

def method_select_transactions(data):
     id = data['user_id']
     try:
          cur.execute("SELECT market,side,volume,price,work_time FROM transactions WHERE active = true AND user_id = %s ORDER BY trans_id DESC",(id,))
     except Exception as ex:
          # print('method_select_transactions err ', ex)
          return json.dumps({'errMsg':ex}), 400, {'Content-Type':'application/json'}
     else:
          transactions_list = cur.fetchall()
          # print('method_select_transactions',transactions_list)
          
          new_transactions_list = list()
          for i in range(0,len(transactions_list)):
               transactions_dict = dict()
               transactions_dict['market'] = transactions_list[i][0]
               transactions_dict['side'] = transactions_list[i][1]
               transactions_dict['volume'] = transactions_list[i][2]
               transactions_dict['price'] = transactions_list[i][3]
               transactions_dict['work_time'] = transactions_list[i][4].strftime("%Y-%m-%d %H:%M:%S")
               new_transactions_list.append(transactions_dict)
               
     return json.dumps({'result':new_transactions_list}), 200, {'Content-Type':'application/json'}


def method_select_wallet(data):
     token = data["sessionToken"]
     decoded = jwt.decode(token, key, algorithms="HS256")
     id = decoded["id"]
     
     try:
          cur.execute("SELECT wallet,privatekey FROM admins WHERE id = %s",(id,))
     except Exception as ex:
          # print('method_select_wallet err',ex)
          return json.dumps({'errMsg':ex}), 400, {'Content-Type':'application/json'}
     else:
          wallet_info = cur.fetchone()
          wallet_dict = dict()
          wallet_dict['wallet'] = wallet_info[0]
          wallet_dict['privatekey'] = wallet_info[1]
          
     return json.dumps({'result':wallet_dict}), 200, {'Content-Type':'application/json'}


def method_select_onetoone():
     try:
          cur.execute("SELECT id, username, email, phone, title, questions, update_time FROM onetoone ORDER BY id DESC")
     except Exception as ex:
          print('method_select_onetoone err',ex)
     else:
          onetoone_info = cur.fetchall()
          onetoone_list = list()
          for i in range(0,len(onetoone_info)):
               data_dict = dict()
               data_dict['id'] = onetoone_info[i][0]
               data_dict['username'] = onetoone_info[i][1]
               data_dict['email'] = onetoone_info[i][2]
               data_dict['phone'] = onetoone_info[i][3]
               data_dict['title'] = onetoone_info[i][4]
               data_dict['questions'] = onetoone_info[i][5]
               data_dict['update_time'] = onetoone_info[i][6].strftime("%Y-%m-%d %H:%M:%S")
               onetoone_list.append(data_dict)
          
     return json.dumps({'result':onetoone_list}), 200, {'Content-Type':'application/json'}


def method_user_point_voucher_info(data):
     
     user_id = data['user_id']
     
     try:
          cur.execute("SELECT SUM(voucher), SUM(used_voucher) FROM voucher WHERE user_id = %s",(user_id,))
     except Exception as ex:
          print('method_user_point_voucher_info err', ex)
     else:
          temp = cur.fetchone()
          voucher = temp[0]
          used_voucher = temp[1]
          left_voucher = voucher - used_voucher
          
     try:
          cur.execute("SELECT SUM(provided_p), SUM(used_p) FROM yb_point WHERE user_id = %s",(user_id,))
     except Exception as ex:
          print('method_user_point_voucher_info err', ex)
     else:
          temp = cur.fetchone()
          provided_p = temp[0]
          used_p = temp[1]
          left_point = provided_p + used_p
          
     currency_info = dict()
     currency_info['voucher'] = left_voucher
     currency_info['point'] = left_point
          
          
     return json.dumps({'result':currency_info}), 200, {'Content-Type':'applcation/json'}
          
          



          
def method_user_refund_info():
     
     try:
          cur.execute(""" select users.id, users.email,users.phone as "phone", 
                    sum(voucher.voucher) as "vouhcer",sum(voucher.used_voucher) 
                    as "used_voucher",sum(yb_point.provided_p) as "point" ,sum(yb_point.used_p) 
                    as "used_p" from users left outer join voucher on (users.id = voucher.user_id) 
                    left outer join yb_point on (users.id = yb_point.user_id) group by 1 order by users.id desc""")
     except Exception as ex:
          print('method_user_point_info err',ex)
          return json.dumps({'errMsg':ex}), 400, {'Content-Type':'application/json'}
     else:
          user_refund_info = cur.fetchall()
          new_user_refund_info = list()
          user_id_list = list()
          for i in range(0,len(user_refund_info)):
               temp = dict()
               temp['id'] = user_refund_info[i][0]
               user_id_list.append(user_refund_info[i][0])
               temp['email'] = user_refund_info[i][1]
               temp['phone'] = user_refund_info[i][2]
               voucher = user_refund_info[i][3]
               used_voucher = user_refund_info[i][4]
               point = user_refund_info[i][5]
               used_p = user_refund_info[i][6]
          
               if voucher == None:
                    voucher = 0.0
               if used_voucher == None:
                    used_voucher = 0.0
               if point == None:
                    point = 0.0
               if used_p == None:
                    used_p = 0.0
          
               voucher = float(voucher)
               used_voucher = float(used_voucher)
               point = float(point)
               used_p = float(used_p)
               
               new_voucher = voucher - used_voucher
               new_point = point + used_p
               temp['voucher'] = new_voucher
               temp['point'] = new_point
               new_user_refund_info.append(temp)
          
     return json.dumps({'result':new_user_refund_info}), 200, {'Content-Type':'application/json'}

def method_member_withdrwal(data):
     user_id = data['id']
     try:
          cur.execute("DELETE FROM users WHERE id = %s",(user_id,))
     except Exception as ex:
          print('method_member_withdrwal err',ex)
          conn.rollback()
     else:
          conn.commit()
          
     return json.dumps({'result':'success'}), 200, {'Content-Type':'application/json'}