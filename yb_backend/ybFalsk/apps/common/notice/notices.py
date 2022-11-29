from ..dbConn import dbConn
import json
from time import strftime

conn = dbConn()
cur = conn.cursor()

def notice_res(notice_type,title,description):
     try:
          cur.execute('INSERT INTO notice(notice_type,title,description) VALUES (%s,%s,%s)',(notice_type,title,description))
     except Exception as ex:
          print('notice_res',ex)
          conn.rollback()
     else:
          conn.commit()
          pass
     
     return json.dumps({'resutl':'success'}), 200 ,{'Content-Type':'application/json'}

def notice_edit(id,notice_type,title,description):
     try:
          cur.execute('UPDATE notice SET(notice_type,title,description) = (%s,%s,%s) WHERE id=%s',(notice_type,title,description,id))
     except Exception as ex:
          print('notice_res',ex)
          conn.rollback()
     else:
          conn.commit()
          pass
     return json.dumps({'resutl':'success'}), 200 ,{'Content-Type':'application/json'}

def notice_list():
     temp = []
     try:
          cur.execute('SELECT * FROM notice WHERE active = True')
     except Exception as ex:
          print('notice_list',ex)
          conn.rollback()
     else:
          temp = cur.fetchall()

     if len(temp) == 0:
          return ({'result':'등록된 공지사항이 없습니다.','notice_type':'','title':'등록된 공지사항이 없습니다.'},)

     tempList = []
     for i in range(0,len(temp)):
          tempdict = dict()
          tempdict['id'] = temp[i][0]
          tempdict['notice_type'] = temp[i][1]
          tempdict['title'] = temp[i][2]
          tempdict['description'] = temp[i][3]
          updatedate = temp[i][4]
          tempdict['date'] = updatedate.strftime("%Y-%m-%d")
          tempList.append(tempdict)

     return tempList

def notice_hide(id):
     try:
          cur.execute('UPDATE notice SET active = False WHERE id = %s',(id,))
     except Exception as ex:
          conn.rollback()
     else:
          conn.commit()
          pass

     # temp = []
     # try:
     #      cur.execute('SELECT * FROM notice WHERE active = True')
     # except Exception as ex:
     #      print('notice_list',ex)
     #      conn.rollback()
     # else:
     #      temp = cur.fetchall()

     # if len(temp) == 0:
     #      return json.dumps({'result':'등록된 공지사항이 없습니다.'}), 200, {'ContentType':'application/json'}

     # tempList = []
     # for i in range(0,len(temp)):
     #      tempdict = dict()
     #      tempdict['id'] = temp[i][0]
     #      tempdict['notice_type'] = temp[i][1]
     #      tempdict['title'] = temp[i][2]
     #      tempdict['description'] = temp[i][3]
     #      updatedate = temp[i][4]
     #      tempdict['date'] = updatedate.strftime("%Y-%m-%d")
     #      tempList.append(tempdict)
     return json.dumps({'result':'success'}),200 ,{'Content-Type':'application/json'}