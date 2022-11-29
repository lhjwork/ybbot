from .dbConn import dbConn
import json
from flask import redirect,url_for
from web3 import Web3

conn = dbConn()
cur = conn.cursor()


def wallet_select(user_id):

     temp = dict()
     try:
          cur.execute('SELECT wallet_add FROM users WHERE id =%s',(user_id,))
     except Exception as ex:
          print('ex',ex)
     else:
          temp = cur.fetchone()
          
     admin_temp = dict()   
     try:
          cur.execute('SELECT wallet FROM admins')
     except Exception as ex:
          print('ex',ex)
     else:
          admin_temp = cur.fetchone()
          

     return {'walletAdd' : temp[0],'admin_wallet':admin_temp[0]}


def wallet_update(user_id,wallet_add):

     search_addr= Web3().isAddress(wallet_add)
     if search_addr == False:
          return redirect(url_for('view_mypage',errMsg='인증된 지갑주소가 아닙니다.' ,error='addr_error'))
     
     try:
          cur.execute('UPDATE users SET wallet_add = %s WHERE id = %s',(wallet_add,user_id))
     except Exception as ex:
          print('ex',ex)
          conn.rollback()
     else:
          conn.commit()
          pass

     return redirect('/mypage')

     
