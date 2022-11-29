from ..dbConn import dbConn
import json 

conn = dbConn()
cur = conn.cursor()


def qna_list():
     temp = []
     try:
          cur.execute('SELECT * FROM question WHERE active = TRUE ')
     except Exception as ex:
          print('ex',ex)
          conn.rollback()
     else:
          temp = cur.fetchall()
          pass 

     if len(temp) == 0:
          return ({'q_type':'[전체]','title':'등록된 질문이 없습니다.','description':'등록된 질문이 없습니다.'},)

     templist = []

     for i in range(0,len(temp)):
          tempdict = dict()
          tempdict['q_id'] = temp[i][0]
          tempdict['q_type'] = temp[i][1]
          tempdict['title'] = temp[i][2]
          tempdict['description'] = temp[i][3]
          # tempdict['answer'] = temp[i][5]
          templist.append(tempdict)
          
     return templist 


def qna_res(q_type,user_id,title,description):
     
     try:
          cur.execute('INSERT INTO question(q_type,user_id,title,description) VALUES(%s,%s,%s,%s)',(q_type,user_id,title,description))
     except Exception as ex:
          print('ex',ex)
          conn.rollback()
     else:
          conn.commit()
          pass

     temp = []
     try:
          cur.execute('SELECT * FROM question WHERE active = TRUE ')
     except Exception as ex:
          print('ex',ex)
          conn.rollback()
     else:
          temp = cur.fetchall()
          pass 

     if len(temp) == 0:
          return json.dumps({'result':'질문사항이 없습니다.'}), 200, {'ContentType':'application/json'}

     templist = []

     for i in range(0,len(temp)):
          tempdict = dict()
          tempdict['q_id'] = temp[i][0]
          tempdict['q_type'] = temp[i][1]
          tempdict['user_id'] = temp[i][2]
          tempdict['title'] = temp[i][3]
          tempdict['description'] = temp[i][4]
          tempdict['answer'] = temp[i][5]
          templist.append(tempdict)

     return templist


def qna_edit(q_id,q_type,title,description):
     try:
          cur.execute('UPDATE question SET (q_type,title,description)=(%s,%s,%s) WHERE q_id =%s',(q_type,title,description,q_id))
     except Exception as ex:
          print('80', ex)
          conn.rollback()
     else:
          conn.commit()
          pass

     temp = []
     try:
          cur.execute('SELECT * FROM question WHERE active = TRUE ')
     except Exception as ex:
          print('ex',ex)
          conn.rollback()
     else:
          temp = cur.fetchall()
          pass 

     if len(temp) == 0:
          return json.dumps({'result':'질문사항이 없습니다.'}), 200, {'ContentType':'application/json'}

     templist = []

     for i in range(0,len(temp)):
          tempdict = dict()
          tempdict['q_id'] = temp[i][0]
          tempdict['q_type'] = temp[i][1]
          tempdict['user_id'] = temp[i][2]
          tempdict['title'] = temp[i][3]
          tempdict['description'] = temp[i][4]
          tempdict['answer'] = temp[i][5]
          templist.append(tempdict)

     return templist



def qna_hide(q_id):
     
     try:
          cur.execute('UPDATE question SET active = FALSE WHERE q_id =%s',(q_id,))
     except Exception as ex:
          print('120', ex)
          conn.rollback()
     else:
          conn.commit()
          pass

     temp = []
     try:
          cur.execute('SELECT * FROM question WHERE active = TRUE ')
     except Exception as ex:
          print('ex',ex)
          conn.rollback()
     else:
          temp = cur.fetchall()
          pass 

     if len(temp) == 0:
          return json.dumps({'result':'질문사항이 없습니다.'}), 200, {'ContentType':'application/json'}

     templist = []

     for i in range(0,len(temp)):
          tempdict = dict()
          tempdict['q_id'] = temp[i][0]
          tempdict['q_type'] = temp[i][1]
          tempdict['user_id'] = temp[i][2]
          tempdict['title'] = temp[i][3]
          tempdict['description'] = temp[i][4]
          tempdict['answer'] = temp[i][5]
          templist.append(tempdict)

     return templist
