import psycopg2

DB_NAME = "ybbot"
DB_USER = "ybbot"
DB_PASS = "12341234"
DB_HOST = "15.164.45.203"
DB_PORT = "5432" 

def dbConn():
     dbconn = psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
     return dbconn

conn = dbConn()
cur = conn.cursor()

def user_info_email(email):
     try:
          cur.execute("SELECT id FROM users WHERE email = %s",(email,))
     except Exception as ex:
          print('user_info_email err',ex)
     else:
          user_id = cur.fetchone()
          
     return user_id

def user_api_info(user_id):
     try:
          cur.execute("SELECT apikey,secretkey FROM users WHERE id = %s",(user_id,))
     except Exception as ex:
          print('user_api_info err',ex)
     else:
          api_info = cur.fetchone()
          api_info_dict = dict()
          api_info_dict['apikey'] = api_info[0]
          api_info_dict['secretkey']  = api_info[1]
     return api_info_dict