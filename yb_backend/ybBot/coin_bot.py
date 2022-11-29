
import time
import json
import requests
from datetime import datetime
import psycopg2
import math

from commons.dbConnFetch import select_erc_tokens
from pytz import timezone, utc



KST = timezone('Asia/Seoul')
now = datetime.now(KST)

check_time = now.strftime('%H:%M:%S')



DB_NAME = "ybbot"
DB_USER = "ybbot"
DB_PASS = "12341234"
DB_HOST = "15.164.45.203"
DB_PORT = "5432"

conn = psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
cur = conn.cursor()

# --> ybbot_set
infura ="https://etherscan.io/address/0xbd79D57518AC16C52c5A92E43787995Cc0766cD2#tokentxns"
admin_address = '0x8351F1D01c61667782f9D240652173E264BAcbFc'
contract_address = "0xEF3fe36b97ea0db5D3e535D10906fefb723b6Cde"

# infura = "https://ropsten.etherscan.io/address/0xbd79D57518AC16C52c5A92E43787995Cc0766cD2#tokentxns"
# admin_address = '0xbd79D57518AC16C52c5A92E43787995Cc0766cD2'
# contract_address = "0x0339A5b356E41E5e9fbbcCF33f9f5B2A155f44db"
api_key = "MVWQ13BRC1P64JP21U3U137GNERBX493EF"
token_unit = math.pow(10,18)
currency_unit = math.pow(10,16)


while True:
     

     # db에 저장된 erc_token 불러오기
     db_trans_list = select_erc_tokens()
     db_trans_count = len(db_trans_list)
     page = db_trans_count / 100
     page = math.ceil(page)
     last_index = db_trans_count - 1
     if last_index == -1 or last_index == 0 or last_index == None:
          db_last_trans = "no trans"
          db_last_hash = "no trans"
     else:
          db_last_trans = db_trans_list[last_index]
          db_last_hash = db_last_trans[1]

     # time.sleep(10000)



     # 신규 데이터 저장 
     # ethersacn에 실시간으로 transaction data 조회
     response = requests.get(f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={contract_address}&address={admin_address}&page={page}&offset=100&startblock=0&endblock=99999999&sort=asc&apikey={api_key}")
     trans_list= response.json()['result']
     for i in range(0,len(trans_list)):
          if db_last_hash == trans_list[i]['hash']:
               for k in range(i+1, len(trans_list)):
                    hash = trans_list[k]['hash']
                    contract_addr = trans_list[k]['contractAddress']
                    from_addr = trans_list[k]['from']
                    trans_time = trans_list[k]['timeStamp']
                    to_addr = trans_list[k]['to']
                    value = trans_list[k]['value']
                    value = float(value)
                    # 임의 currency -->yb_set
                    currency = value/currency_unit
                    trans_time = datetime.fromtimestamp(int(trans_time)).strftime('%Y-%m-%d %H:%M:%S')
                    try:
                         cur.execute('INSERT INTO erc_tokentxns(hash,contract_addr,from_add,to_add,value,trans_time,currency) VALUES (%s,%s,%s,%s,%s,%s,%s)',(hash,contract_addr,from_addr,to_addr,value,trans_time,currency))
                    except Exception as ex:
                         conn.rollback()
                    else:
                         conn.commit()


          # db에 있는 value 및 point 지급 유무값 확인
          try:
               cur.execute('SELECT erc_id,hash,from_add,to_add,value,currency FROM erc_tokentxns where p_provided = false')
          except Exception as ex:
               print('select erc_tokentxns',ex)
          else:
               deposit_list = cur.fetchall()

               for i in range(0,len(deposit_list)):

                    erc_id = deposit_list[i][0]
                    hash = deposit_list[i][1]
                    # remittance_addr : 송금주소
                    remittance_addr = deposit_list[i][2]
                    deposit_addr = deposit_list[i][3]
                    # 입금 주소 -> 어드민에 해당해야함
                    coin_value = deposit_list[i][4]
                    currency = deposit_list[i][5]


                    if deposit_addr == admin_address:
                         try:
                              cur.execute('SELECT id,email FROM users WHERE wallet_add = %s',(remittance_addr,))
                         except Exception as ex:
                              print('select remittance_addr err', ex)
                         else:
                              user_info = cur.fetchone()
                              user_id = user_info[0]
                              payment_p =coin_value / token_unit

                              # 포인트 등록
                              try:
                                   cur.execute('INSERT INTO yb_point(user_id,provided_p,hash,currency) VALUES (%s,%s,%s,%s)',(user_id,payment_p,hash,currency))
                              except Exception as ex:
                                   conn.rollback()
                              else:
                                   conn.commit()

                                   try:
                                        cur.execute('UPDATE erc_tokentxns SET p_provided = True WHERE erc_id = %s AND hash = %s',(erc_id,hash))
                                   except Exception as ex:
                                        conn.rollback()
                                   else:
                                        conn.commit()

          # value 만큼 point 지급



     

