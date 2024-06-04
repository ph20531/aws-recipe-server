from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt, jwt_required, create_access_token
from mysql_connection import getConnection
from mysql.connector import Error
from email_validator import EmailNotValidError, validate_email
from utils import encryption, decryption
from utils import isEmpty

# ______________________________________________________________________________________
# 인증 토큰 | 서버 > 클라이언트 | create_access_token()
# ______________________________________________________________________________________

# 인증 토큰 유효기간 설정하는 방법
# 001 | API에서 설정
#     | from datetime import timedelta
#     | access_token = create_access_token(user_id, expires_delta=timedelta(seconds=10))
# ______________________________________________________________________________________
# 002 | config.py에서 수정
#     | JWT_ACCESS_TOKEN_EXPIRES = 10

class UserRegisterResource(Resource):
    def post(self):
        # - body
        data = request.get_json()
        
        if isEmpty(data, 'username', 'email', 'password'):
            # ERROR | 400
            return {
                'result': 'fail',
                'error': '400 bad request. The request was invalid.'
                }, 400
        
        try:
            validate_email(data['email'])
        except EmailNotValidError as e:
            # ERROR | 400
            return {
                'result': 'fail',
                'error': str(e)
                }, 400
        
        password_length = len(data['password'])
        min_limit_length, max_limit_length = 4, 12
        if password_length < min_limit_length or password_length > max_limit_length:
            # ERROR | 400
            return {
                'result': 'fail',
                'error': f'400 bad request. Password must be between {min_limit_length} and {max_limit_length} characters.'
                }, 400
        
        # - database
        try:
            connection = getConnection()

            query = '''INSERT INTO user (username, email, password) VALUES (%s, %s, %s);'''
            args = (data['username'], data['email'], encryption(data['password']))

            cursor = connection.cursor()

            cursor.execute(query, args)
            connection.commit()

            # 인증 토큰 | 001. user테이블에 INSERT된 후 해당 데이터의 user_id값을 가져와야 한다.
            user_id = cursor.lastrowid

            cursor.close()
            connection.close()
        except Error as e:
            if cursor is not None:
                cursor.close()

            if connection is not None:
                connection.close()

            # ERROR | 500
            return {
                'result':'fail',
                'error':str(e)
                }, 500
        
        # 인증 토큰 | 002. user_id로 액세스 토큰 생성
        access_token = create_access_token(user_id)
        
        # SUCCESS | 200
        return {
            'result':'success',
            'access_token':access_token # 인증 토큰 | 003. 꼭 클라이언트에 access_token값을 보내줘야 한다.
            }, 200
    
class UserLoginResource(Resource):
    def post(self):
        # - body
        data = request.get_json()
        
        if isEmpty(data, 'email', 'password'):
            # ERROR | 400
            return {
                'result': 'fail',
                'error': '400 bad request. The request was invalid.'
                }, 400
        
        try:
            validate_email(data['email'])
        except EmailNotValidError as e:
            # ERROR | 400
            return {
                'result': 'fail',
                'error': str(e)
                }, 400
        
        password_length = len(data['password'])
        min_limit_length, max_limit_length = 4, 12
        if password_length < min_limit_length or password_length > max_limit_length:
            # ERROR | 400
            return {
                'result': 'fail',
                'error': f'400 bad request. Password must be between {min_limit_length} and {max_limit_length} characters.'
                }, 400
        
        # - database
        try:
            connection = getConnection()

            query = '''SELECT * FROM user WHERE email = %s;'''
            args = (data['email'],)

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, args)

            result = cursor.fetchall()

            cursor.close()
            connection.close()
        except Error as e:
            if cursor is not None:
                cursor.close()

            if connection is not None:
                connection.close()

            # ERROR | 500
            return {
                'result':'fail',
                'error':str(e)
                }, 500
        
        if not result:
            # ERROR | 400
            return {
                'result': 'fail',
                'error':  'bad request. The user does not exist.'
                }, 400
        
        if not decryption(data['password'], result[0]['password']):
            # ERROR | 400
            return {
                'result': 'fail',
                'error':  'bad request. The password does not match.'
                }, 400
        
        # 인증 토큰 | 001. 로그인 후 user_id값을 가져와야 한다.
        user_id = result[0]['id']

        # 인증 토큰 | 002. user_id로 액세스 토큰 생성
        access_token = create_access_token(user_id)

        # SUCCESS | 200
        return {
            'result':'success',
            'access_token':access_token # 인증 토큰 | 003. 꼭 클라이언트에 access_token값을 보내줘야 한다.
            }, 200

# 로그아웃된 토큰들을 저장할 Set 생성
# Set | 중복이 허용되지 않음
jwt_blacklist = set()
class UserLogoutResource(Resource):
    @jwt_required()
    def delete(self):
        jti = get_jwt()['jti']
        jwt_blacklist.add(jti)
        return {
            'result':'success'
            }, 200