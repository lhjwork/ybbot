from .dbConn import *
import jwt
import json

conn = dbConn()
cur = conn.cursor()


key = "ybbot_secert"

def method_update_wallet(data):
     token = data["sessionToken"]
     wallet = data["wallet"]
     privatekey = data['privatekey']
     decoded = jwt.decode(token, key, algorithms="HS256")
     id = decoded["id"]

     try:
          cur.execute("UPDATE admins SET wallet = %s, privatekey = %s WHERE id = %s",(wallet,privatekey,id))
     except Exception as ex:
          print('select_transactions err',ex)
          conn.rollback()
     else:
          conn.commit()
          
     
     return json.dumps({'reuslt':'success'}), 200, {"Content-Type":"application/json"}

def method_notice_update(data):
     id = data['id']
     notice_type = data['notice_type']
     title = data['title']
     description = data['description']
     try:
          cur.execute("UPDATE notice SET (notice_type,title,description) = (%s,%s,%s) WHERE notice_id = %s",(notice_type,title,description,id))
     except Exception as ex:
          # print('ex',ex)
          conn.rollback()
     else:
          conn.commit()
          
     return json.dumps({'result':'success'}), 200, {'Content-Type':'application/json'}

def method_question_update(data):
     id = data['id']
     notice_type = data['q_type']
     title = data['title']
     description = data['description']
     try:
          cur.execute("UPDATE question SET (q_type,title,description) = (%s,%s,%s) WHERE q_id = %s",(notice_type,title,description,id))
     except Exception as ex:
          # print('ex',ex)
          conn.rollback()
     else:
          conn.commit()
          
     return json.dumps({'result':'success'}), 200, {'Content-Type':'application/json'}

def method_question_delete(data):
     id = data['id']
     try:
          cur.execute("UPDATE question SET active = false WHERE q_id = ANY(%s)",(id,))
     except Exception as ex:
          # print('ex',ex)
          conn.rollback()
     else:
          conn.commit()
          
     return json.dumps({'result':'success'}), 200, {'Content-Type':'application/json'}