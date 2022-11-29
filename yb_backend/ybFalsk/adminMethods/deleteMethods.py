import json
from .dbConn import *


conn = dbConn()
cur = conn.cursor()

def method_notice_delete(data):
     id = data['id']
     try:
          cur.execute("UPDATE notice SET active = false WHERE notice_id = ANY(%s)",(id,))
     except Exception as ex:
          print('method_notice_delete err',ex)
          conn.rollback()
     else:
          conn.commit()
     return json.dumps({'result':'success'}), 200, {'Content-Type':'application/json'}

