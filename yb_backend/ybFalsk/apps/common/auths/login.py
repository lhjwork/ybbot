from ..dbConn import dbConn
from .model_user import *
from flask import redirect, render_template
from flask_login import login_user
import json
import re

conn = dbConn()
cur = conn.cursor()

def login_handler(email,password):

     if email != 'jin.come.up.business@gmail.com':

          if (len(password)<7):
               error_statement = '비밀번호는 8자리 이상이어야 합니다.'
               return render_template('login.html',error_statement =error_statement,err_modal = None )


          if not re.findall('[a-z]',password) or not re.findall('[0-9]+',password):
               error_statement = '비밀번호 기준(숫자, 영문 구성)에 맞지 않습니다.'
               return render_template('login.html',error_statement =error_statement ,err_modal = None)
          


          if not re.findall('[!@$#*]+',password):
               error_statement = '비밀번호는 최소 1개 이상의 특수문자가 포함되어야 합니다.'
               return render_template('login.html',error_statement =error_statement ,err_modal = None)
               # raise TypeError('비밀번호는 최소 1개 이상의 특수문자가 포함되어야 합니다.')
          
          

          try:
               cur.execute('SELECT password FROM users WHERE email=%s',(email,))
          except Exception as ex:
               print('38',ex)
               conn.rollback() 
          else:
               try:
                    saved_password = cur.fetchone()[0]
               except Exception as ex:
                    saved_password = 'email_error'
     
          if saved_password == 'email_error': 
               error_statement = '이메일을 확인 바랍니다.'
               return render_template('login.html',error_statement =error_statement,err_modal = None)

          if sha256_crypt.verify(password,saved_password):
               #사용자가 입력한 정보가 회원가입된 사용자인지 확인
               user_info = User.get_user_info(email)
     
               login_info = User(user_id=user_info['user_id'],email=user_info['email'],phone=user_info['phone'],username=user_info['username'],accessKey = user_info['accessKey'],secretKey = user_info['secretKey'])

               login_user(login_info)
     
               return redirect('/main')
          else:
               error_statement = '비밀번호가 일치하지 않습니다.'
               return render_template('login.html',error_statement =error_statement, err_modal = None )
     else:
          try:
               cur.execute('SELECT password FROM users WHERE email=%s',(email,))
          except Exception as ex:
               print('38',ex)
               conn.rollback()
          else:
               saved_password = cur.fetchone()[0]
          if sha256_crypt.verify(password,saved_password):
               #사용자가 입력한 정보가 회원가입된 사용자인지 확인
               user_info = User.get_user_info(email)
     
               login_info = User(user_id=user_info['user_id'],email=user_info['email'],phone=user_info['phone'],username=user_info['username'],accessKey = user_info['accessKey'],secretKey = user_info['secretKey'])

               login_user(login_info)

               return redirect('/main')
          else:
               error_statement = '비밀번호가 일치하지 않습니다.'
               return render_template('login.html',error_statement =error_statement, err_modal = None ) 
