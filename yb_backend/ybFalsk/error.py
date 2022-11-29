from flask import Flask,g,request,render_template,redirect,url_for,session,jsonify,abort
from werkzeug.exceptions import HTTPException, default_exceptions, _aborter

def JsonApp(app):
    def error_handling(error):
        if isinstance(error, HTTPException):  # HTTP Exeption의 경우
            result = {
                'code': error.code,
                'description': error.description,
                'message': str(error)
            
            }
        else:
            description = _aborter.mapping[500].description # 나머지 Exception의 경우
            result = {
                'code': 500,
                'description': description,
                'message': str(error)
            }
        resp = jsonify(result)
        resp.status_code = result['code']
        return resp
        
    for code in default_exceptions.keys(): # 에러 핸들러 등록 
        app.register_error_handler(code, error_handling)

    return app
