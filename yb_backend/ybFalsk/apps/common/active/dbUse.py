from ybBot.commons.requests import current_trade_price
from flask import redirect,url_for
from ..dbConn import dbConn
import json
conn = dbConn()
cur = conn.cursor()

# def user_active_start(user_id,trans_type):
#      print('user_id user_active_start',user_id)

#      try:
#           cur.execute("SELECT start_active FROM users WHERE id = %s",(user_id,))
#      except Exception as ex:
#           print('user_active_start',ex)
#           return {'errMsg':ex}, 400
#      else:
#           cur_active = cur.fetchone()[0]

#      if cur_active == True:
#           try:
#                cur.execute("UPDATE users SET start_active = false WHERE id = %s", (user_id,))
#           except Exception as ex:
#                conn.rollback()
#                # print('ex:',ex)
               
#                return {'errMsg':ex}, 400
#           else:
#                conn.commit()
#                pass
#                return redirect(url_for('view_main',page='main'))

#      else:
#           try:
#                cur.execute("UPDATE users SET start_active = true WHERE id = %s", (user_id,))
#           except Exception as ex:
#                conn.rollback()
#                # print('ex:',ex)
               
#                return {'errMsg':ex}, 400
#           else:
#                conn.commit()
#                pass
#                return redirect(url_for('view_main',page='main'))
def user_api_info(user_id):
     try:
          cur.execute("SELECT apikey,secretkey FROM users WHERE id = %s",(user_id,))
     except Exception as ex:
          print('user_api_info err',ex)
     else:
          api_info = cur.fetchone()
          api_info_dict = dict()
          api_info_dict['apikey'] = api_info[0]
          api_info_dict['secretkey']  = api_info[1]
     return api_info_dict



def user_voucher_info(user_id):
     try:
          cur.execute("SELECT SUM(voucher), SUM(used_voucher) FROM voucher WHERE user_id = %s AND NOW() <= finish_time ",(user_id,))
     except Exception as ex:
          print('user_api_info err',ex)
     else:
          voucher_info = cur.fetchone()
          voucher_info_dict = dict()
          voucher_info_dict['voucher'] = voucher_info[0]
          voucher_info_dict['used_voucher']  = voucher_info[1]
     return voucher_info_dict



def user_active_start(user_id,trans_type):
     
     api_info_dict = user_api_info(user_id)
     user_vouchers = user_voucher_info(user_id)
     
     if user_vouchers['voucher'] == None or user_vouchers['used_voucher'] == None:
          return redirect(url_for('view_transaction',res = 'error',errMsg = '이용권이 부족합니다.'))
     elif user_vouchers['voucher'] - user_vouchers['used_voucher'] <= 0:
          return redirect(url_for('view_transaction',res = 'error',errMsg = '이용권이 부족합니다.'))
     
     if api_info_dict['apikey'] == None or api_info_dict['secretkey'] == None:
          return redirect(url_for('view_transaction',res = 'error',errMsg = 'apiKey,secretkey 등록이 필요합니다.'))

     if api_info_dict['apikey'] == None or api_info_dict['secretkey'] == None:
          return redirect()
     if trans_type == None:
          try:
               cur.execute("UPDATE users SET start_active = true, invest_type = 'attack0' WHERE id = %s",(user_id,))
          except Exception as ex:
               print('user_active_start err',ex)
               conn.rollback()
          else:
               conn.commit()
               
               return redirect('/loading')
     else:
          try:
               cur.execute("UPDATE users SET start_active = true, invest_type = %s WHERE id = %s",(trans_type,user_id))
          except Exception as ex:
               print('user_active_start err',ex)
               conn.rollback()
          else:
               conn.commit()
               return redirect('/loading')



def user_voucher_active_start(user_id):
     try:
          cur.execute("SELECT start_active FROM users WHERE id = %s",(user_id,))
     except Exception as ex:
          print('user_active_start',ex)
          return {'errMsg':ex}, 400
     else:
          cur_active = cur.fetchone()[0]

     if cur_active == True:
          try:
               cur.execute("UPDATE users SET start_active = false WHERE id = %s", (user_id,))

          except Exception as ex:
               conn.rollback()
               # print('ex:',ex)
               
               return {'errMsg':ex}, 400
          else:
               conn.commit()
               cur_start_active = False
               pass
               return redirect(url_for('view_voucher',page='voucher',active_status = cur_start_active))

     else:
          try:
               cur.execute("UPDATE users SET start_active = true WHERE id = %s", (user_id,))
          except Exception as ex:
               conn.rollback()
               # print('ex:',ex)
               
               return {'errMsg':ex}, 400
          else:
               conn.commit()
               cur_start_active = True
               pass
               return redirect(url_for('view_voucher',page='voucher',active_status = cur_start_active))

def user_mypage_active_start(user_id):
     try:
          cur.execute("SELECT start_active FROM users WHERE id = %s",(user_id,))
     except Exception as ex:
          print('user_active_start',ex)
          return {'errMsg':ex}, 400
     else:
          cur_active = cur.fetchone()[0]

     if cur_active == True:
          try:
               cur.execute("UPDATE users SET start_active = false WHERE id = %s", (user_id,))
          except Exception as ex:
               conn.rollback()
               # print('ex:',ex)
               
               return {'errMsg':ex}, 400
          else:
               conn.commit()
               cur_start_active = False
               pass
               return redirect(url_for('view_mypage',page='mypage',active_status = cur_start_active))

     else:
          try:
               cur.execute("UPDATE users SET start_active = true WHERE id = %s", (user_id,))
          except Exception as ex:
               conn.rollback()
               # print('ex:',ex)
               
               return {'errMsg':ex}, 400
          else:
               conn.commit()
               cur_start_active = True
               pass
               return redirect(url_for('view_mypage',page='mypage',active_status = cur_start_active))



def cur_active_start_status(user_id):
     try:
          cur.execute("SELECT start_active FROM users WHERE id = %s",(user_id,))
     except Exception as ex:
          print('cur_active_start_status err',ex)
     else:
          cur_start_active = cur.fetchone()[0]
     
     return cur_start_active

def method_stop(user_id):
     
     api_info_dict = user_api_info(user_id)
     if api_info_dict['apikey'] == None or api_info_dict['secretkey'] == None:
          return redirect(url_for('view_transaction',res = 'error',errMsg = 'apiKey,secretkey 등록이 필요합니다.'))
     
     try:
          cur.execute("UPDATE users SET start_active = false WHERE id = %s",(user_id,))
     except Exception as ex:
          print('method_stop err',ex)
          conn.rollback()
     else:
          conn.commit()
     
     return redirect('/loading')



def user_alarm(user_id):
     try:
          cur.execute("SELECT invest_type,start_active FROM users WHERE id = %s ",(user_id,))
     except Exception as ex:
          print('user_alarm err',ex)
     else:
          user_invest_info = cur.fetchone()
          data_dict = dict()
          data_dict['type'] = user_invest_info[0]
          data_dict['active'] = user_invest_info[1]
          
     return data_dict