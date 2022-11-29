from ..dbConn import dbConn
import json

conn = dbConn()
cur = conn.cursor()


def start_active_update(user_id,startActive):
     try:
          cur.execute('UPDATE users SET startActive = %s WHERE id = %s',(startActive,user_id))
     except Exception as ex:
          print('start_active_update',ex)
          conn.rollback()
     else:
          conn.commit()
     return json.dumps({'result':'success'}), 200, {'Content-Type':'application/json'}