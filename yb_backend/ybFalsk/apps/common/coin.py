from .dbConn import dbConn
from flask import render_template


conn = dbConn()
cur = conn.cursor()

def method_user_point_voucher(user_id):
     user_voucher= ''
     try:
          cur.execute("SELECT SUM(voucher),SUM(used_voucher) FROM voucher WHERE NOW() <= finish_time AND user_id = %s",(user_id,))
     except Exception as ex:
          user_voucher = 0
          remain_point = 0
          return {'user_voucher': user_voucher,'remain_point': remain_point}
     else:
          user_voucher = cur.fetchall()
     
          temp_data = user_voucher[0]
          if temp_data[0] == None:
               user_voucher = 0.0
          else:
               user_voucher = temp_data[0]
               
          if temp_data[1] == None:
               used_voucher = 0.0
          else:
               used_voucher = temp_data[1]
          
          user_voucher = user_voucher - used_voucher
          
     try:
          cur.execute("SELECT SUM(provided_p), SUM(used_p) FROM yb_point WHERE user_id = %s",(user_id,))
     except Exception as ex:
          return render_template("voucher.html")
     else:
          try:
               user_point_info = cur.fetchone()
               remain_point = user_point_info[0] + user_point_info[1]
          except Exception as ex:
               user_voucher = 0
               remain_point = 0
               return {'user_voucher': user_voucher,'remain_point': remain_point}
          else:
               pass
     return {'user_voucher': user_voucher,'remain_point': remain_point}


def remain_point(user_id):
     try:
          cur.execute('SELECT sum(provided_p),sum(used_p),sum(currency) FROM yb_point WHERE user_id = %s',(user_id,))
     except Exception as ex:
          # print('remain_voucher ex',ex)
          raise TypeError(ex)
     else:
          point_dict = dict()
          point_list = cur.fetchall()
          sum_provided_p = point_list[0][0]
          sum_used_p = point_list[0][1]
          sum_currency = point_list[0][2]
          if sum_provided_p == None or sum_currency == None:
               remain_point = 0
               sum_currency = 0
          else:
               remain_point = sum_provided_p + sum_used_p

          point_dict = {'remain_point':remain_point,'seven_currency':sum_currency,'remain_currency':sum_currency}

     return point_dict

