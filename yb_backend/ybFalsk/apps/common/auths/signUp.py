from crypt import methods
from email import header
from flask import redirect,url_for
from flask_cors import cross_origin
from passlib.hash import sha256_crypt
import jwt
import json
import requests
import re

from ..dbConn import dbConn

conn = dbConn()
cur = conn.cursor()


def signUp(username,password,phone,email):


     if len(password)<7:
          error_statement = '비밀번호는 8자리 이상이어야 합니다.'
          return redirect(url_for('view_join_signupform_mailcheck',signupform='email_check', email=email,username=username,phone=phone,error_statement=error_statement))

     
     if not re.findall('[a-z]',password) or not re.findall('[0-9]+',password):
          error_statement = '비밀번호 기준(숫자, 영문 구성)에 맞지 않습니다. 소문자를 포함해 주세요. '
          return redirect(url_for('view_join_signupform_mailcheck',signupform='email_check', email=email,username=username,phone=phone,error_statement=error_statement))


     if not re.findall('[!@$#*]+',password):
          error_statement = '비밀번호는 최소 1개 이상의 특수문자가 포함되어야 합니다.'
          return redirect(url_for('view_join_signupform_mailcheck',signupform='email_check', email=email,username=username,phone=phone,error_statement=error_statement))


     if(len(phone) != 11):
          error_statement = '전화번호 자릿수를 확인바랍니다.'
          return redirect(url_for('view_join_signupform_mailcheck',signupform='email_check', email=email,username=username,phone=phone,error_statement=error_statement))



     #email 정보 없을때 써칭이 유효 처리 필요

     password = sha256_crypt.encrypt(password)
     try:
          cur.execute("UPDATE users SET (username,password,phone) = (%s, %s, %s) WHERE email = %s", (username,password,phone,email))
     except Exception as ex:
          conn.rollback()
          # print('ex:',ex)
          return {'errMsg':ex}, 400
     else:
          conn.commit()
          pass
     
     try:
          cur.execute("SELECT id FROM users where email =%s",(email,))
     except Exception as ex:
          print('SELECT id FROM users where email err',ex)
     else:
          temp_id = cur.fetchone()[0]

     try:
          cur.execute("INSERT INTO yb_point(user_id,provided_p,used_p) VALUES(%s,%s,%s)",(temp_id,0,0))
     except Exception as ex:
          conn.rollback()
          # print('ex:',ex)
          return {'errMsg':ex}, 400
     else:
          conn.commit()
          pass
     
     try:
          cur.execute("INSERT INTO voucher(user_id,voucher,used_voucher) VALUES(%s,%s,%s)",(temp_id,0,0))
     except Exception as ex:
          conn.rollback()
          # print('ex:',ex)
          return {'errMsg':ex}, 400
     else:
          conn.commit()
          pass
     
     
          
     return redirect('/join_complete')
