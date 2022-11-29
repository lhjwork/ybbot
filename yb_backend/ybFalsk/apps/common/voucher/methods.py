
import json
from this import d 
import pytz
from time import gmtime, strftime
import datetime
import psycopg2
from flask import redirect,url_for,render_template

DB_NAME = "ybbot"
DB_USER = "ybbot"
DB_PASS = "12341234"
DB_HOST = "15.164.45.203"
DB_PORT = "5432" 

def dbConn():
     dbconn = psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
     return dbconn

    # dt = dt.strftime("%Y-%m-%d %H:%M:%S")


conn = dbConn()
cur = conn.cursor()

def method_purchase_voucher(user_id,used_to_p,currency):
    currency =currency.replace(',','')
    currency = int(currency.replace('₩',''))
    try:
        cur.execute("SELECT SUM(provided_p),SUM(used_p) FROM yb_point WHERE user_id = %s",(user_id,))
    except Exception as ex:
        print('method_purchase_voucher err',ex)
        return {'errMsg',ex}, 400
    else:
        user_points = cur.fetchone()
        provided_p = user_points[0]
        used_p = user_points[1]
        used_to_p = float(used_to_p)
        
        if provided_p == None:
            provided_p = 0
        if used_p == None:
            used_p = 0 

        if provided_p + used_p <= used_to_p:
            # # return render_template('login.html',error_statement =error_statement ,err_modal = None)
            # return render_template('voucher.html',error_statement ='포인트가 부족합니다.' ,res = 'error')
            return redirect(url_for('view_voucher',errMsg = '포인트가 부족합니다.',res = 'error'))
    
        try:
            cur.execute("INSERT INTO voucher(user_id,voucher) VALUES(%s,%s)",(user_id,used_to_p))
        except Exception as ex:
            print('method_purchase_voucher err',ex)
            conn.rollback()
        else:
            conn.commit()
        
        try:
            cur.execute("INSERT INTO yb_point(user_id,used_p,currency) VALUES(%s,%s,%s)",(user_id,-used_to_p,currency))
        except Exception as ex:
            print('method_purchase_voucher err',ex)
            conn.rollback()
        else:
            conn.commit()
            
        return redirect(url_for('view_voucher'))

def method_user_voucher(user_id):
    temp = list()
    try:
        cur.execute("SELECT SUM(voucher),SUM(used_voucher) FROM voucher WHERE NOW() < finish_time AND user_id = %s",(user_id,))
    except Exception as ex:
        return {'errMsg':ex}
    else:
        temp = cur.fetchone()
        user_voucher = temp[0]
        used_voucher = temp[1]
        
        if temp[0] == None:
            user_voucher = 0.0
            
        if temp[1] == None:
            used_voucher = 0.0
            
        
        user_voucher = user_voucher - used_voucher
        
    return {'user_voucher':user_voucher}


def method_purchase_list_voucher(user_id):
    user_voucher_list = list()
    format_ = '%Y-%m-%d %H:%M:%S'
    try:
        cur.execute("SELECT voucher,update_time FROM voucher WHERE user_id = %s AND NOW() <= finish_time AND 0 < voucher ORDER BY update_time DESC ",(user_id,))
    except Exception as ex:
        return {'errMsg':ex}
    else:
        user_voucher_list = cur.fetchall()
        new_user_voucher_list = list()
        for i in range(0,len(user_voucher_list)):
            voucher_dict = dict()
            voucher_dict['voucher_p'] = user_voucher_list[i][0]
            voucher_dict['update_time'] = user_voucher_list[i][1].strftime('%Y-%m-%d %H:%M:%S')
            # dt_strptime = datetime.datetime.strptime(time, format_)
            # # next_time = dt_strptime + datetime.timedelta(hours=-3)
            # voucher_dict['update_time'] = dt_strptime.strftime('%Y-%m-%d %H:%M:%S')
            new_user_voucher_list.append(voucher_dict)
            
    return new_user_voucher_list