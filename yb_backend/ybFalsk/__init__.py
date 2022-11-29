# ybFalsk 모듈의 시작 지점 -> __init__: 생성자를 뜻함
# 모듈이 구동되면 __init__.py는 자동으로 실행된다.
# Flask(대문자임으로 class 형식임을 알 수 있다.)
# application context:나한테 접속하는 모든 사람들에게 공유하는 공간
# session context: 나만 사용하는 공간(내정보를 담는 공간)

from crypt import methods
from flask import Flask,g,request,render_template,redirect,url_for,session,jsonify,abort
from werkzeug.exceptions import HTTPException, default_exceptions, _aborter
from flask_login import LoginManager, current_user
from flask_login import login_user, logout_user,login_required
# import os
# import jwt
# import uuid
# import hashlib
import json
import pytz
import pyupbit as ub

# test
# from urllib.parse import urlencode
from passlib.hash import sha256_crypt

from .apps.common.quotation import quo_orderbook
from .apps.common.notice.notices import notice_hide,notice_list,notice_res
from .apps.common.QnA.qna import qna_list,qna_res,qna_edit,qna_hide
# from  .apps.common.keyupdate import keyupdate
from .apps.common.key_use.key_use import * 
from .apps.common.wallet_api import *

from .apps.common.auths.emailVertification import *
from .apps.common.auths.login import login_handler
from .apps.common.auths.signUp import signUp
from .apps.common.auths.emailCheck import emailCheck
from .apps.common.auths.model_user import User
from .apps.common.auths.startActive import start_active_update

from .apps.common.balancegraph.balances import *
from .apps.common.ask_bid.passdata import pass_bid,pass_ask
from .apps.common.ask_bid.orders import *
from .apps.common.dbConn import *
from .apps.common.coin import *
from .apps.common.active.dbUse import *
from .apps.common.voucher.methods import * 
from .apps.common.oneToOne.dbUse import *
from .error import JsonApp
# import requests
from flask_cors import CORS, cross_origin
from flask_mail import Mail
from flask_mail import Message
from email_validator import validate_email, EmailNotValidError


app = JsonApp(Flask(__name__))

mail = Mail(app)

CORS(app)
app.debug = True
app.secret_key ='ybbot1234'

# db 관련 
conn = dbConn()
cur =conn.cursor() # conn roll back 시 사용

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = "jin.use.email@gmail.com"
app.config['MAIL_PASSWORD'] = "zkpypgjagymhwujq"
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

#flask_login 라이브러리의 로그인 관련 기능을 담고 있는 로그인 객체이다. Flask 객체로 생성한 어플리케이션(ex.app) 을 연결한다.
login_manager = LoginManager()
login_manager.init_app(app)  # app 에 login_manager 연결

# flask_login에서 제공하는 login_required를 실행하기 전 사용자 정보를 조회한다.
@login_manager.user_loader
def user_loader(email):
     
    # 사용자 정보 조회
    user_info = User.get_user_info(email)
    # user_loader함수 반환값은 사용자 '객체'여야 한다.
#     # 결과값이 dict이므로 객체를 새로 생성한다.
#     login_info = User(user_id=user_info['data'][0]['USER_ID'])
    login_info = User(user_id=user_info['user_id'],email=user_info['email'],phone=user_info['phone'],username=user_info['username'],accessKey = user_info['accessKey'],secretKey = user_info['secretKey'])
    return login_info
# re

# login_required로 요청된 기능에서 현재 사용자가 로그인되어 있지 않은 경우
# unauthorized 함수를 실행한다.
@login_manager.unauthorized_handler
def unauthorized():
    # 로그인되어 있지 않은 사용자일 경우 첫화면으로 이동
    return redirect("/")


app.before_request
def defore_request():
     g.str ="all_request"


#=======================html temple 관련 부분================================
@app.route('/')
def view_login():
     err_modal = request.args.get('err_modal')
     return render_template("login.html", err_modal=err_modal)

@app.route('/<form>')
def view_login_form(form):
     err_modal = request.args.get('err_modal')
     return render_template("login.html", err_modal=err_modal,res=form)

@app.route('/repassword/<repassAuth>', methods=['GET','POST'])
def view_repassword_repassAuth(repassAuth):
     email = request.args.get('email')
     return render_template("login.html", email=email, res=repassAuth)

#test
@app.route('/join')
def view_join():
     return render_template("join.html")

@app.route('/join/<signupform>')
def view_join_signupform(signupform):
     email = request.args.get('email')
     username= request.args.get('username')
     phone = request.args.get('phone')
     error_statement = request.args.get('error_statement')
     return render_template("join.html",res = signupform,email=email,username=username,phone=phone, error_statement=error_statement)

@app.route('/join/<signupform>')
def view_join_signupform_mailcheck(signupform):
     email = request.args.get('email')
     username= request.args.get('username')
     phone = request.args.get('phone')
     verificationCode = request.args.get('verificationCode')
     error_statement = request.args.get('error_statement')
     
     return render_template("join.html",res = signupform,verificationCode=verificationCode,email=email,username=username,phone=phone,error_statement=error_statement)


#test
@app.route('/join_complete')
def view_join_complete():
     return render_template("join_complete.html")

@app.route('/business_information')
def view_business_information():
     return render_template("business_information.html")

@app.route('/terms_use')
def view_terms_use():
     return render_template("terms_use.html")

@app.route('/privacy_policy')
def view_privacy_policy():
     return render_template("privacy_policy.html")

@app.route('/contact_us')
def view_contact_us():
     return render_template("contact_us.html")

@app.route('/main')
def view_main():
     list = notice_list()[0]
     try:
          user_id = current_user.user_id
          username = current_user.username
     except:
          return render_template("main2.html")
     else:
          pass
          user_voucher = method_user_voucher(user_id)
          active_status = cur_active_start_status(user_id)
          alarm_info = user_alarm(user_id)
     # email=session['_user_id']
     #current_user로 사용자 정보 불러오기 확인
     
     return render_template("main.html",username=username, notice_list=list,voucher_info=user_voucher,active_status=active_status,alarm_info=alarm_info)

@app.route('/main/<parameter>')
def view_main_active_url(parameter):
     try:
          list = notice_list()[0]
          user_id = current_user.user_id
          user_voucher = method_user_voucher(user_id)
          page = request.args.get('page')
          username = current_user.username
     except:
          return redirect('/main')
     else:
          return render_template("main.html",parameter=parameter,username=username, notice_list=list,voucher_info=user_voucher,page=page)


@app.route('/start_active',methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def api_active_start():
     if request.method == 'POST':
          user_id = current_user.user_id
          trans_type = request.form.get('trans_type')
          print('trans_type 202',trans_type)
          return user_active_start(user_id,trans_type)
     
@app.route('/stop',methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def api_stop():
     if request.method == 'GET':
          user_id = current_user.user_id
          return method_stop(user_id)
     
@app.route('/active_start_voucher',methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def api_active_start_voucher():
     if request.method == 'GET':
          user_id = current_user.user_id
          return user_voucher_active_start(user_id)

@app.route('/active_start_mypage',methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def api_active_start_mypage():
     if request.method == 'GET':
          user_id = current_user.user_id
          return user_mypage_active_start(user_id)
     
@app.route('/alarm',methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def api_alarm():
     if request.method == 'GET':
          user_id = current_user.user_id
          return user_alarm(user_id)

@app.route('/mypage')
def view_mypage():
  
     try:
          user_id = current_user.user_id
          username = current_user.username
     except:
          return redirect('/')
     else:
          wallet_add = wallet_select(user_id)
          accessKey = accessKey_select(user_id)
          week_datas = week_profit_datas(user_id)
          week_datas = week_datas[0]
          week_datas_list = week_datas['week_data_list']
          max_profit_rate = week_datas['max_profit_rate']
          user_point_voucher = method_user_point_voucher(user_id)
          active_status = cur_active_start_status(user_id)
          alarm_info = user_alarm(user_id)
          
          errMsg = request.args.get('errMsg')
          error = request.args.get('error')
          res = request.args.get('res')

          return render_template("mypage.html", wallets = wallet_add,alarm_info=alarm_info, week_datas = week_datas_list,max_profit_rate = max_profit_rate,user_point_voucher = user_point_voucher,accessKey=accessKey, username=username,page='mypage',active_status=active_status,errMsg=errMsg,error=error,res=res)

@app.route('/mypage/<parameter>')
def view_mypage_active_start(parameter):
 
     try:
          user_id = current_user.user_id
          username = current_user.username
     except:
          return redirect('/')
     else:
          wallet_add = wallet_select(user_id)
          accessKey = accessKey_select(user_id)
          week_datas = week_profit_datas(user_id)
          week_datas = week_datas[0]
          week_datas_list = week_datas['week_data_list']
          max_profit_rate = week_datas['max_profit_rate']
          user_point_voucher = method_user_point_voucher(user_id)
          page = request.args.get('page')
    
          
     return render_template("mypage.html",parameter=parameter, user_wallet = wallet_add, week_datas = week_datas_list,max_profit_rate = max_profit_rate,user_point_voucher = user_point_voucher,accessKey=accessKey, username=username,page=page)


@app.route('/manual')
def view_menual():
     return render_template("manual.html")

@app.route('/business_list')
def view_business_list():
     try:
          user_id = current_user.user_id
          access_key = current_user.accessKey
          secret_key = current_user.secretKey
     except:
          return redirect('/')
     else:
          if access_key == None or secret_key == None:
               error_statement = 'key 등록이 필요합니다.'
               bid_datas = []
               return render_template("business_list.html",orders=[],completions=[], error_statement=error_statement)

          try:
          # bid_datas = bid_history(access_key,secret_key)
               # completion_datas= completion_order(access_key,secret_key,user_id)
               completion_datas = completion_order_real(user_id)
          except:
               return redirect('/business_list')
          else:
               pass


          if type(completion_datas) == type(dict()):
               error_statement = '올바른 key를 등록해주세요.'
               return render_template("business_list.html",orders=[],completions=[], error_statement=error_statement)
          
          #선택 화면에서 주문에 해당하는 리스트 값
          try:
               bid_datas = current_bid_order_marketValue_real(user_id)
               print('bid_datas',bid_datas)
          except:
               return redirect('/business_list')
          else:
          # bid_datas = current_bid_order_marketValue(access_key,secret_key,user_id)
               return render_template("business_list.html",orders=bid_datas, completions=completion_datas)

@app.route('/order_list')
def view_order_list():
     return render_template("order_list.html")

@app.route('/faq_list')
def view_faq_list():
     list = qna_list()
     return render_template("faq.html", qna_list=list)

@app.route('/transaction')
def view_transaction():
     errMsg = request.args.get('errMsg')
     res = request.args.get('res')
     return render_template("transaction.html",errMsg=errMsg,res=res)

@app.route('/transaction_complete')
def view_transaction_complete():
     return render_template("transaction_complete.html")

@app.route('/voucher')
def view_voucher():
     try:
          username = current_user.username
          user_id = current_user.user_id
     except:
          return redirect('/')
     else:
          user_point_voucher = method_user_point_voucher(user_id)
          active_status = cur_active_start_status(user_id)
          errMsg = request.args.get('errMsg')
          res = request.args.get('res')
          return render_template("voucher.html", username=username, user_point_voucher=user_point_voucher,page='voucher',active_status=active_status, res = res, errMsg = errMsg)

@app.route('/voucher/<parameter>')
def view_voucher_active_start(parameter):

     try:
          username = current_user.username
          user_id = current_user.user_id
     except:
          return redirect('/')
     else:
          user_point_voucher = method_user_point_voucher(user_id)
          page = request.args.get('page')
     
          return render_template("voucher.html",parameter=parameter,username=username, user_point_voucher=user_point_voucher,page=page)



@app.route('/purchase_list')
def view_purchase_list():
     try:
          user_id = current_user.user_id
     except:
          return redirect('/')
     else:
          purchase_list = method_purchase_list_voucher(user_id)
          return render_template("purchase_list.html", purchase_list=purchase_list)

@app.route('/notice_list', methods=['GET','POST'])
def init_notice_list():
     notices = notice_list()
     return render_template('notice.html', notice_list=notices)

@app.route('/loading')
def view_loading():
     try:
          user_id = current_user.user_id
     except:
          return redirect('/')
     else:
          alarm_info = user_alarm(user_id)
          return render_template("loading.html",alarm_info=alarm_info)
# # 로그인 실패 시 재로그인
# @app.route('/relogin')
# def relogin():
#      login_result_text = "로그인에 실패했습니다. 다시 시도해주세요."
#      # return render_template('', login_result_text=login_result_text)
#      return '임시 로그인 실패 시 재로그인 경로'
# 로그아웃
@app.route('/logout')
def logout():
    # session 정보를 삭제한다.
    logout_user()
#   login 페이지
    return redirect('/')

#======================================================================


# 호가 정보 불러오기 ticker:KRW-BTC,BTC-ET
@app.route('/orderbook/<ticker>',methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def quotation_orderboo(ticker):
     if request.method =='GET':
          temp =  quo_orderbook(ticker)
          return json.dumps({"my_all_account":temp}), 200, {'ContentType':'application/json'}





@app.route('/bidpass', methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def api_bid_pass():
     if request.method == 'POST':
          data = dict()
          data = request.get_json()
          price = data['price']
          tickers = data['tickers']
          accessKey = data['accessKey']
          secretKey = data['secretKey']
          split_step = data['split_step']
          panic_step = data['panic_step']
          user_id = data['user_id']
          auto_set = data['auto_set']
          # pass_bid(accessKey,secretKey,price,tickers,split_step,panic_step,user_id) 
          return pass_bid(accessKey,secretKey,price,tickers,split_step,panic_step,user_id,auto_set)

@app.route('/bidsend',methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def bid_get():
     if request.method == 'POST':
          data_json = dict()
          # try:
          data_json = request.get_json()
          accessKey = data_json['accessKey']
          secretkey = data_json['secretKey']
          price = data_json['price']
          tickers = data_json['tickers']
          split_step = data_json['split_step']
          panic_step = data_json['panic_step']
          user_id = data_json['user_id']

          #bid_order(apikey,secretkey,volume,price,side,tickers):
          result_order = bid_order(accessKey,secretkey,price,tickers,split_step,panic_step,user_id)

          return result_order

@app.route('/askpass', methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def ask_pass():
     if request.method == 'POST':
          data = dict()
          try:
               data = request.get_json()
          except Exception as ex:
               return json.dumps({'errMsg':ex}), 400, {'Content-Type':'application/json'}

          price = data['volume']
          trade_price = data['trade_price']
          ticker = data['ticker']
          accessKey = data['accessKey']
          secretKey = data['secretKey']
          avg_bid_price = data['avg_bid_price']
          auto_set = data['auto_set']
          user_id = data['user_id']
          
          # pass_ask(accessKey,secretKey,volume,price,tickers,avg_bid_price,user_id)
          pass_ask(price,trade_price,ticker,accessKey,secretKey,avg_bid_price,auto_set,user_id)

     return json.dumps({'result':'success'}), 200, {'Content-Type':'application/json'}


@app.route('/asksend',methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def ask_get():
     if request.method == 'POST':
          # try:
          data = request.get_json()

          volume = data['volume']
          trade_price = data['trade_price']
          ticker = data['ticker']
          accessKey = data['accessKey']
          secretkey = data['secretKey']
          user_id = data['user_id']
          avg_bid_price = data['avg_bid_price']
          
          result_order = ask_order(volume,trade_price,accessKey,ticker,secretkey,avg_bid_price,user_id)
     
          return json.dumps({'result':result_order}), 200, {'Content-Type':'application/json'}
#================================================Auth====================================================

@app.route('/emailverification',methods=['GET','POST'])
def init_emailverification():
     if request.method =='POST':
          username = request.form.get('username')
          phone = request.form.get('phone')
          email = request.form.get('email')
          username = username.strip()
          phone = phone.strip()
          email = email.strip()
          return emailverification(email,username,phone)

@app.route('/emailcheck', methods=['GET','POST'])
def api_emailcheck():
     if request.method == 'POST':
          verification = request.form.get('verification')
          email = request.form.get('email')
          username = request.form.get('username')
          phone = request.form.get('phone')
          verification = verification.strip()
          email = email.strip()
          username = username.strip()
          phone = phone.strip()

     return emailCheck(verification,email,username,phone)

@app.route('/password_check',methods=['GET','POST'])
def api_pass_check():
     if request.method == 'POST':
          username = request.form.get('username')
          phone = request.form.get('phone')
          email = request.form.get('email')
          password = request.form.get('password')
          password_chk = request.form.get('password_chk')
          password = password.strip()
          password_chk = password_chk.strip()

          if password == password_chk:
               pass
          else:
               raise TypeError('비밀번호 확인이 일치하지 않습니다.')
          

     return {'result':'success'}, 200


@app.route('/signup', methods=['GET','POST'])
def api_signUp():
     if request.method == 'POST':
          logout_user()
          username = request.form.get('username')
          password = request.form.get('password')
          password_chk = request.form.get('password_chk')
          phone = request.form.get('phone')
          email = request.form.get('email')
          username = username.strip()
          password = password.strip()
          password_chk = password_chk.strip()
          phone = phone.strip()
          if password == password_chk:
               pass
          else:
               error_statement = '비밀번호 확인이 일치하지 않습니다.'
               return redirect(url_for('view_join_signupform_mailcheck',signupform='email_check', email=email,username=username,phone=phone,error_statement=error_statement))

          
          return signUp(username,password,phone,email)


@app.route('/login', methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def api_login():
     if request.method == 'POST':
          email = request.form.get('email')
          password = request.form.get('pwd')
          email = email.strip()
          password = password.strip()
     return login_handler(email,password)

@app.route('/login/<loginform>', methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def api_login_from(loginform):
     if request.method == 'POST':
          email = request.form.get('email')
          password = request.form.get('pwd')
          email = email.strip()
          password = password.strip()
     return login_handler(email,password)


@app.route('/keysupdate', methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def api_keyupdate():
     if request.method == 'POST':
          apikey = request.form.get('accesskey')
          secretkey = request.form.get('secretkey')
          email = current_user.email
          apikey = apikey.strip()
          secretkey = secretkey.strip()
          
          
     return keyupdate(apikey,secretkey,email)


@app.route('/keyinfo', methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def api_keyinfo_get():
     if request.method == 'GET':
          temp = ''
          # email = session['_user_id']
          # temp = keyinfo_get(email)
          return 'keyinfo_success'

@app.route('/wallet_update', methods=['GET','POST'])
def api_wallet_update():
     if request.method == 'POST':
          user_id = current_user.user_id
          wallet_add = request.form.get('walletAdd')
          return wallet_update(user_id,wallet_add)


@app.route('/send_auth_repassnum', methods=['GET','POST'])
def api_repass_emailVertification():
     if request.method == 'POST':
          
          user_email = request.form.get('userEmail')
          user_email = user_email.replace(" " , "")
          try:
               user_email = validate_email(user_email).email
               user_id =user_info_email(user_email)
          except EmailNotValidError as e:
               # email is not valid, exception message is human-readable
               # print(str(e))
               return redirect(url_for('view_login',err_modal = '이메일 주소를 입력바랍니다.',email=user_email, res = 'err_modal'))
          else:
               pass
          if user_id == None:
               return redirect(url_for('view_login',err_modal = '등록된 회원이 아닙니다.',email=user_email,res = 'err_modal'))
          
     return repass_emailverification(user_email)

# set

@app.route('/repass_auth_num_check', methods=['GET','POST'])
def api_repass_auth_num_check():
     if request.method == 'POST':
          try:
               repass_auth_num = request.form.get('authNum')
               email = request.form.get('userEmail')
               email = email.replace(" " , "")
               repass_auth_num = repass_auth_num.replace(" " , "")
          except Exception as ex:
               return redirect('/')
          else:
               pass
     return repass_auth_num_check(repass_auth_num,email)

@app.route('/repass_auth_num_check/<repassform>', methods=['GET','POST'])
def api_repass_auth_num_check_form(repassform):
     if request.method == 'POST':
          try:
               repass_auth_num = request.form.get('authNum')
               email = request.form.get('userEmail')
               error_statement = request.args.get('error_statement')
               # print('error_statement--->',error_statement)
          except Exception as ex:
               # print('repass_auth_num_check err',ex)
               return redirect('/')
          else:
               pass
               email = request.form.get('userEmail')
     return render_template('login.html',res = repassform, error_statement = error_statement,repass_auth_num=repass_auth_num,email = email)

     
@app.route('/repassword',methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def api_repassword():
     if request.method == 'POST':
          receiver_email = request.form.get('userEmail')
          receiver_email = receiver_email.replace(" " , "")
          return repassword(receiver_email)
     
@app.route('/password_change',methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def api_password_change():
     if request.method == 'POST':
          password = request.form.get('password')
          ch_password = request.form.get('ch_password')
          user_id = current_user.user_id
          return method_ch_password(password,ch_password,user_id)


@app.route('/purchase_voucher', methods=['GET','POST'])
def api_purchase_voucher():
     if request.method == 'POST':
          user_id = current_user.user_id
          used_p = request.form.get('used_p')
          currency = request.form.get('currency')
          return method_purchase_voucher(user_id,used_p,currency)
          # return render_template('faq.html',quaList = qnaList) 

# =====================================notice =====================================

@app.route('/notice_res', methods=['GET','POST'])
def api_notice_res():
     if request.method == 'POST':
          notice_type = request.form.get('notice_type')
          title = request.form.get('title')
          description = request.form.get('description')
          # notice_res(notice_type,title,description):
          return notice_res(notice_type,title,description)


     
@app.route('/notice_hide/<notice_id>',methods=['GET,POST'])
def api_notice_hide(notice_id):
     # if request.method == 'GET':
          # print('notice_id',notice_id, type(notice_id))
          notice_hide(notice_id)
          return 'test'


@app.route('/qna_list', methods=['GET','POST'])
def api_qna_list():
     if request.method == 'GET':
          qnaList = qna_list()
          return render_template('faq.html',quaList = qnaList) 


@app.route('/qna_res', methods=['GET','POST'])
def api_qna_res():
     if request.method == 'POST':
          user_id = current_user.user_id
          q_type = request.form.get('q_type')
          title = request.form.get('title')
          description = request.form.get('description')
          qnaList = qna_res(q_type,user_id,title,description)
          return render_template('faq.html',quaList = qnaList) 

#test
@app.route('/qna_edit/<id>', methods=['GET','POST'])
def api_qna_edit(id):
     if request.method == 'POST':
          q_id = id
          # user_id = current_user.id
          q_type = request.form.get('q_type')
          title = request.form.get('title')
          description = request.form.get('description')
          qnaList = qna_edit(q_id,q_type,title,description)

          return render_template('faq.html',quaList = qnaList) 

@app.route('/qna_hide/<id>', methods=['GET','POST'])
def api_qna_hide(id):
     if request.method == 'POST':
          q_id = id
          # user_id = current_user.id
          qnaList = qna_hide(q_id)
          return render_template('faq.html',quaList = qnaList) 

@app.route('/one_to_one', methods=['GET','POST'])
def api_one_to_one():
     if request.method == 'POST':
          username = request.form.get('username')
          email = request.form.get('email')
          phone = request.form.get('phone')
          title = request.form.get('title')
          questions = request.form.get('questions')
          return method_one_to_one_insert(username,email,phone,title,questions)




# ===============================balance=======================
@app.route('/all_account',methods=['GET','POST'])
def api_all_account():
     if request.method == 'GET':
          access_key = current_user.access_key
          secret_key = current_user.secret_key
          # all_accounts(access_key,secret_key):
          temp = all_accounts(access_key,secret_key)
          

          return json.dumps({'result':temp}) , 200, {'Content-Type':'application/json'}


     