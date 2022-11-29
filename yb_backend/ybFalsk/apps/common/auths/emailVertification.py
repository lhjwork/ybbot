from cmath import e
from contextlib import redirect_stderr
from operator import le
import random
from email import header
from flask_cors import cross_origin
import json
import requests
from flask_mail import Mail
from flask_mail import Message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl
from passlib.hash import sha256_crypt
from flask import redirect,url_for,render_template
import re


from ..dbConn import dbConn



conn = dbConn()
cur = conn.cursor()
sender_email = "jin.use.email@gmail.com"
smtp_password = "zkpypgjagymhwujq"

def emailverification(email,username,phone):

          verificationcode = str(random.randint(1000, 9999))

          print('send verificationcode : ',verificationcode)

          receiver_email = email

          message = MIMEMultipart("alternative")
          message["Subject"] = "ybbot 이메일 인증코드"
          message["From"] = sender_email
          message["To"] = receiver_email

          # Create the plain-text and HTML version of your message
          text = """\
          {}
          """.format(verificationcode)
     
          # Turn these into plain/html MIMEText objects
          part1 = MIMEText(text, "plain")
          message.attach(part1)

          # Create secure connection with server and send email
          context = ssl.create_default_context()

          try:
               server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
               server.ehlo()
               server.login(sender_email, smtp_password)
               server.sendmail(
               sender_email, receiver_email, message.as_string()
               )
          except Exception as ex:
               print('ex 54',ex)
               pass
          else:
               pass
          temp = ''
          try:
               cur.execute('SELECT id FROM users WHERE email=%s',(email,))
          except Exception as ex:
               print('68',ex)
          else:
               temp = cur.fetchone()


          if temp:
               try:
                    cur.execute('UPDATE users SET verification=%s WHERE email=%s',(verificationcode,email))
               except Exception as ex:
                    print('update ex',ex)
                    conn.rollback()
               else:
                    conn.commit()
                    pass
          else: 
               try:
                    
                    cur.execute("INSERT INTO users (email, verification) VALUES (%s, %s)",(email, verificationcode))
               except Exception as ex:
                    print('90',ex)
                    conn.rollback()
               else:
                    conn.commit()
                    pass

          # return {"result":'email_update'}, 200
          return redirect(url_for('view_join_signupform',signupform='email_verification',email=email,username=username,phone=phone))


def repass_emailverification(email):
     verificationcode = str(random.randint(1000, 9999))

     print('send verificationcode : ',verificationcode)

     receiver_email = email

     message = MIMEMultipart("alternative")
     message["Subject"] = "ybbot 패스워드 재설정 이메일 인증코드"
     message["From"] = sender_email
     message["To"] = receiver_email

     # Create the plain-text and HTML version of your message
     text = """\
     {}
     """.format(verificationcode)

     # Turn these into plain/html MIMEText objects
     part1 = MIMEText(text, "plain")
     message.attach(part1)

     # Create secure connection with server and send email
     context = ssl.create_default_context()

     try:
          server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
          server.login(sender_email, smtp_password)
          server.sendmail(
          sender_email, receiver_email, message.as_string()
          )
     except Exception as ex:
          print('Exception',ex)
     else:
          pass

     try:
          cur.execute('UPDATE users SET repass_auth_num=%s WHERE email=%s',(verificationcode,email))
     except Exception as ex:
          print('ex',ex)
          conn.rollback()
     else:
          conn.commit()

     # return redirect(url_for('view_repassword_repassAuth', repassAuth='success_authNum'))
     # return url_for('view_repassword_repassAuth', repassAuth='success_authNum'))
     return render_template('login.html', res='success_authNum',email=email)


def repass_auth_num_check(repass_auth_num,email):
     try:
          cur.execute('SELECT repass_auth_num FROM users WHERE email = %s',(email,))
     except Exception as ex:
          print('except',ex)
          return redirect('/')
     else:
          temp = cur.fetchone()
          auth_num = temp[0]

          # print('auth_num,repass_auth_num',auth_num,repass_auth_num)
     
     if auth_num == None:
          return redirect(url_for('view_login',err_modal = '등록되지 않은 가입자입니다.',res = 'repass_err'))
     
     if repass_auth_num != auth_num:
          return render_template('login.html', res='success_authNum',email=email, err_modal = '인증번호를 다시 확인해주세요.')

     try:
          cur.execute('UPDATE users SET repass_auth_res = True WHERE email = %s',(email,))
     except Exception as ex:
          print('ex',ex)
          return redirect('/')
     else:
          conn.commit()
          pass
          return render_template('login.html', res='success_authCheck',email=email, authNum = repass_auth_num)


     # return redirect(url_for('view_repassword_repassAuth',repassAuth='success_authCheck',email=email))

def repassword(receiver_email):
     try: 
          cur.execute('SELECT repass_auth_res FROM users WHERE email=%s',(receiver_email,))
     except Exception as ex:
          print('ex',ex)
     else:
          temp = cur.fetchone()
          auth_res = temp[0]

     if auth_res == False:
          raise TypeError('인증확인이 필요합니다.')
     
     

     lowercase_letters = 'abcdefghijklmnopqrstuvwxyz'
     digits = '0123456789'
     symbols = '!@$#*'

     #비밀번호 구성 선택
     lower, nums, sysms = True, True, True

     all = ""

     all += lowercase_letters + digits + symbols
     # all += digits
     # all += symbols

     length = 8  #비밀번호의 길이
     amount = 2  #비밀번호의 개수

     for i in range(amount):
          password = "".join(random.sample(all,length))
          # print('202',password)

     password = '3' + password + '*' 
     sha256_password = sha256_crypt.encrypt(password)
     # print('207',sha256_password)

     try:
          cur.execute('UPDATE users SET password = %s WHERE email = %s',(sha256_password,receiver_email))
     except Exception as ex:
          print('ex',ex)
          conn.rollback()
     else:
          conn.commit()

     message = MIMEMultipart("alternative")
     message["Subject"] = "ybbot 패스워드를 보내드립니다. "
     message["From"] = sender_email
     message["To"] = receiver_email

     # Create the plain-text and HTML version of your message
     text = """\
     {}
     """.format(password)

     # Turn these into plain/html MIMEText objects
     part1 = MIMEText(text, "plain")
     message.attach(part1)

     # Create secure connection with server and send email
     context = ssl.create_default_context()

     try:
          server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
          server.login(sender_email, smtp_password)
          server.sendmail(
          sender_email, receiver_email, message.as_string()
          )
     except Exception as ex:
          print('Exception',ex)
     else:
          pass

     return redirect(url_for('view_login',))

def method_ch_password(password,ch_password,user_id):
     
     if password != ch_password:
          return redirect(url_for('view_mypage',errMsg='비밀번호가 일치하지 않습니다.',error='ch_error'))
     
     
     if (len(password)<7):
               errMsg = '비밀번호는 8자리 이상이어야 합니다.'
               return redirect(url_for('view_mypage',errMsg=errMsg, error='ch_error'))
     

     if not re.findall('[a-z]',password) or not re.findall('[0-9]+',password):
          errMsg = '비밀번호 기준(숫자, 영문 구성)에 맞지 않습니다.'
          return redirect(url_for('view_mypage',errMsg=errMsg,error='ch_error'))
     

     if not re.findall('[!@$#*]+',password):
          errMsg = '비밀번호는 최소 1개 이상의 특수문자가 포함되어야 합니다.'
          return redirect(url_for('view_mypage',errMsg=errMsg ,error='ch_error'))
     
     
     try:
          cur.execute('UPDATE users SET password = %s WHERE id = %s',(sha256_crypt.encrypt(password),user_id))
     except Exception as ex:
          print('ex',ex)
          conn.rollback()
     else:
          conn.commit()
          
     return redirect(url_for('view_mypage',res='success_ch_pass'))
     