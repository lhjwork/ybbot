from flask import request
from .dbConn import dbConn
import json

conn = dbConn()
cur = conn.cursor()

def keyupdate(apikey,secretkey,email):
     try: 
          cur.execute('UPDATE users SET apikey=%s,secretkey=%s WHERE email=%s',(apikey,secretkey,email)) 
     except Exception as ex:
          print('ex',ex)
          conn.rollback()
     else:
          conn.commit()
          pass

     return json.dumps({'result':'success'}), 200,{'Content-Type':'application/json'}