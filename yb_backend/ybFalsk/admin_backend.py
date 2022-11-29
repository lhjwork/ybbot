from wsgiref import headers
from flask import Flask, request, logging, jsonify, redirect
from flask_cors import CORS, cross_origin
from passlib.hash import sha256_crypt
# from flask_sslify import SSLify


from adminMethods.deleteMethods import *
from adminMethods.InsertMethods import *
from adminMethods.selectMethods import *
from adminMethods.updateMethods import *

import json
import jwt

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
@cross_origin(origins='*',headers=['Content-Type','Authorization'])
def serverTest():
     return 'serverTest'


@app.route('/admin_sign_up', methods=['GET', 'POST'])
@cross_origin(origins='*',headers=['Content-Type','Authorization'])
def api_admin_sign_up():
     if request.method == 'POST':
          try:
               data = request.get_json()
          except Exception as ex:
               print('admin_sign_up api err',ex)
               return json.dumps({'errMsg':ex}), 400, {'Content-Type':'application/json'}
          else:
               pass
          return method_admin_signup(data)


@app.route('/login', methods=['GET', 'POST'])
@cross_origin(origins='*',headers=['Content-Type','Authorization'])
def api_login():
    if request.method == 'POST':
        data = request.get_json()
        try:
            loginId = data['loginId']
            password = data['password']
        except Exception as ex:
            print('api_login err',ex)
            return json.dumps({'errMsg':ex}), 400, {'Content-Type':'application/json'}
        else:
            pass 
            return adminLogin(loginId,password)
       

@app.route('/notice_list', methods=['GET', 'POST'])
@cross_origin(origins='*',headers=['Content-Type','Authorization'])
def api_notice_list():
     if request.method == 'GET':
          return method_notice_list()

@app.route('/notice_insert', methods=['GET', 'POST'])
@cross_origin(origins='*',headers=['Content-Type','Authorization'])
def api_notice_insert():
     if request.method == 'POST':
          try:
               data = request.get_json()
          except Exception as ex:
               json.dumps({'errMsg':ex}),400, {'Content-Type':'application/json'}
          else:
               pass
          return method_notice_insert(data)
     
     
@app.route('/notice_update', methods=['GET', 'POST'])
@cross_origin(origins='*',headers=['Content-Type','Authorization'])
def api_notice_update():
     if request.method == 'POST':
          try:
               data = request.get_json()
          except Exception as ex:
               json.dumps({'errMsg':ex}),400, {'Content-Type':'application/json'}
          else:
               pass
          return method_notice_update(data)    

@app.route('/notice_delete', methods=['GET', 'POST'])
@cross_origin(origins='*',headers=['Content-Type','Authorization'])
def api_notice_delete():
     if request.method == 'POST':
          try:
               data = request.get_json()
          except Exception as ex:
               json.dumps({'errMsg':ex}),400, {'Content-Type':'application/json'}
          else:
               pass
          return method_notice_delete(data) 


@app.route('/user_list', methods=['GET', 'POST'])
@cross_origin(origins='*',headers=['Content-Type','Authorization'])
def api_user_list():
     if request.method == 'GET':
          return method_user_list()

@app.route('/transcation_list', methods=['GET', 'POST'])
@cross_origin(origins='*',headers=['Content-Type','Authorization'])
def api_transcation_list():
     if request.method == 'POST':
          try:
               data = request.get_json()
          except Exception as ex:
               print('api_transcation_list err', ex)
          else:
               pass
               return method_select_transactions(data)
          
          
@app.route('/question_list', methods=['GET', 'POST'])
@cross_origin(origins='*',headers=['Content-Type','Authorization'])
def api_question_list():
     if request.method == 'GET':
          return method_select_question()
     
@app.route('/question_insert', methods=['GET', 'POST'])
@cross_origin(origins='*',headers=['Content-Type','Authorization'])
def api_question_insert():
     if request.method == 'POST':
          try:
               data = request.get_json()
          except Exception as ex:
               print('api_transcation_list err', ex)
          else:
               pass
          return method_question_insert(data)

@app.route('/question_update', methods=['GET', 'POST'])
@cross_origin(origins='*',headers=['Content-Type','Authorization'])
def api_question_update():
     if request.method == 'POST':
          try:
               data = request.get_json()
          except Exception as ex:
               print('api_question_update err', ex)
          else:
               pass
          return method_question_update(data)

@app.route('/question_delete', methods=['GET', 'POST'])
@cross_origin(origins='*',headers=['Content-Type','Authorization'])
def api_question_delete():
     if request.method == 'POST':
          try:
               data = request.get_json()
          except Exception as ex:
               print('api_question_delete err', ex)
          else:
               pass
          return method_question_delete(data)


@app.route('/select_transactions', methods=['GET', 'POST'])
@cross_origin(origins='*',headers=['Content-Type','Authorization'])
def api_select_transactions():
     if request.method == 'POST':
          try:
               data = request.get_json()
          except Exception as ex:
               print('api_select_transactions err', ex)
          else:
               pass
          return method_select_transactions(data)
     
@app.route('/wallet_update', methods=['GET', 'POST'])
@cross_origin(origins='*',headers=['Content-Type','Authorization'])
def api_update_wallet():
     if request.method == 'POST':
          try:
               data = request.get_json()
          except Exception as ex:
               print('api_update_wallet err', ex)
          else:
               pass
          return method_update_wallet(data)   


@app.route('/admin_wallet_info', methods=['GET', 'POST'])
@cross_origin(origins='*',headers=['Content-Type','Authorization'])
def api_wallet_info():
     if request.method == 'POST':
          try:
               data = request.get_json()
          except Exception as ex:
               print('api_update_wallet err', ex)
          else:
               pass
          return method_select_wallet(data)

@app.route('/point_refund', methods=['GET', 'POST'])
@cross_origin(origins='*',headers=['Content-Type','Authorization'])
def api_point_refund():
     if request.method == 'POST':
          try:
               data = request.get_json()
          except Exception as ex:
               print('api_point_refund err', ex)
          else: 
               pass
          return method_ybPoint_refund(data)
     
     
@app.route('/point_provide', methods=['GET', 'POST'])
@cross_origin(origins='*',headers=['Content-Type','Authorization'])
def api_point_provide():
     if request.method == 'POST':
          try:
               data = request.get_json()
          except Exception as ex:
               print('api_point_provide err', ex)
          else: 
               pass
          return method_ybPoint_provide(data)


# 
@app.route('/onetoone_list', methods=['GET', 'POST'])
@cross_origin(origins='*',headers=['Content-Type','Authorization'])
def api_select_onetoone():
     if request.method == 'GET':
          return method_select_onetoone()
     
@app.route('/refund_list', methods=['GET', 'POST'])
@cross_origin(origins='*',headers=['Content-Type','Authorization'])
def api_refund_list():
     if request.method == 'GET':
          return method_user_refund_info()
     
@app.route('/point_voucher_info', methods=['GET', 'POST'])
@cross_origin(origins='*',headers=['Content-Type','Authorization'])
def api_user_point_voucher_info():
     if request.method == 'POST':
          try:
               data = request.get_json()
          except Exception as ex:
               print('pi_user_point_voucher_info err',ex)
          else:
               pass          
          return method_user_point_voucher_info(data)


@app.route('/member_withdrwal', methods=['GET', 'POST'])
@cross_origin(origins='*',headers=['Content-Type','Authorization'])
def api_member_withdrwal():
     if request.method == 'POST':
          try:
               data = request.get_json()
          except Exception as ex:
               print('pi_user_point_voucher_info err',ex)
          else:
               pass          
          return method_member_withdrwal(data)






if __name__ == '__main__':
     app.secret_key='secret123'
     app.run(host='0.0.0.0', port=5500, debug=True)