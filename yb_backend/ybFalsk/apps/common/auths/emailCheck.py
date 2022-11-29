import requests
from ..dbConn import dbConn
import json
from flask import redirect,url_for

conn = dbConn()
cur = conn.cursor()

def emailCheck(verification,email,username,phone):
 
     try:
          cur.execute('SELECT id FROM users WHERE phone = %s',(phone,))
     except Exception as ex:
          # print('ex',ex)
          conn.rollback()
     else:
          there_is_user = cur.fetchone()
          
     try:
          cur.execute('SELECT id FROM users WHERE email = %s',(email,))
     except Exception as ex:
          # print('ex',ex)
          conn.rollback()
     else:
          there_is_user_2 = cur.fetchone()
          
     if there_is_user == None or there_is_user_2 == None:
          temp = ''
          try:
               cur.execute('SELECT verification FROM users WHERE email=%s',(email,))
          except Exception as ex:
               # print('14',ex)
               conn.rollback()
          else:
               temp = cur.fetchone()[0]
               # print('19',temp)
               pass
               
          if verification != temp: 
               error_statement = '인증번호가 일치하지 않습니다.'
               return redirect(url_for('view_join_signupform',signupform='email_verification',email=email,username=username,phone=phone, error_statement=error_statement))

          
          try:
               cur.execute('UPDATE users SET registered=TRUE WHERE email=%s',(email,))
          except Exception as ex:
               conn.rollback()
          else:
               conn.commit()
               pass
     else:
          error_statement = '이메일또는 휴대전화가 가입되어 있습니다.'
          return redirect(url_for('view_join_signupform',signupform='email_verification',email=email,username=username,phone=phone, error_statement=error_statement))

     return redirect(url_for('view_join_signupform_mailcheck',signupform='email_check', email=email,username=username,phone=phone,verification=verification))
