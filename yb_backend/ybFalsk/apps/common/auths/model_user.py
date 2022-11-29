# flask_login에서 제공하는 사용자 클래스 객체
from traceback import print_tb
from flask_login import UserMixin
from ..dbConn import dbConn
from passlib.hash import sha256_crypt

conn = dbConn()
cur = conn.cursor()


# UserMixin 상속하여 flask_login에서 제공하는 기본 함수들 사용
class User(UserMixin):
     def __init__(self,user_id,email,phone,username,accessKey,secretKey):
          self.user_id = user_id
          self.email = email
          self.phone = phone
          self.username = username
          self.accessKey = accessKey
          self.secretKey = secretKey

     # def get_email(self):
     #      return str(self.email)

     def get_id(self):
          return self.email

     def __repr__(self):
          return f"USER : {self.user_id} = {self.email}"

# User객체를 생성하지 않아도 사용할 수 있도록 staticmethod로 설정
# 사용자가 작성한 계정 정보가 맞는지 확인하거나
# flask_login의 user_loader에서 사용자 정보를 조회할 때 사용한다.

     @staticmethod
     def get_user_info(email):
               temp_dict = dict()
               try:
                    cur.execute('SELECT*FROM users WHERE email=%s',(email,))
               except Exception as ex:
                    print('35 model_user',ex)
               else:
                    temp = cur.fetchone()
                    pass
                    temp_user_id = temp[0]
                    temp_username = temp[1]
                    temp_phone = temp[2]
                    temp_email = temp[4]
                    temp_access_key = temp[6]
                    temp_secret_key = temp[7]
                    temp_dict['user_id'] = temp_user_id
                    temp_dict['username'] = temp_username
                    temp_dict['phone'] = temp_phone
                    temp_dict['email'] = temp_email
                    temp_dict['accessKey'] = temp_access_key
                    temp_dict['secretKey'] = temp_secret_key
               return temp_dict
               

               






