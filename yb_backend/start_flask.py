# __init__.py를 구동하는 파일
# 메모리에 띄우는 역활
# __init__.py은 자동으로 구성되어 있기 때문에 경로를 생략하고 바로 호출 가능, app을 불러왔다.
# ybFalsk 모듈을 대표하는 것이라고 생각하면 된다.
from ybFalsk import app


if __name__ == '__main__':
# default : 5000
     app.run(host='0.0.0.0',debug=True) #127.0.0.1 == localhost