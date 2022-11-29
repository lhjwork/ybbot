import jwt
import hashlib
import os
import requests
import uuid
from urllib.parse import urlencode, unquote
from ybBot.commons.checkStock import view_krw_items
import json
import pandas as pd
import time
from datetime import datetime
from pytz import timezone, utc
import psycopg2


DB_NAME = "ybbot"
DB_USER = "ybbot"
DB_PASS = "12341234"
DB_HOST = "15.164.45.203"
DB_PORT = "5432"

conn = psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
cur = conn.cursor()



KST = timezone('Asia/Seoul')




# access_key = 'xxrHjO3rbgxjYCIHxj1nDmR3oxPyCO126j4LlhkX'
# secret_key = 'gRFkcQp8sz4tERMEeiwgmM2BC2F4WgfxxnJodCQu'
# server_url = 'https://api.upbit.com'


 


while True:
      test = view_krw_items()





