from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import jwt_blacklist
from config import Config

# flask와 flask-restful 라이브러리 설치
# flask run 명령어로 실행이 안될 경우
# set FLASK_APP=003_FLASK\app.py 명령어로 패스 설정

from resources.base import BaseHTTPResource
from resources.recipe import RecipesResource, RecipesByIdResource, RecipesPublishByIdResource
from resources.user import UserRegisterResource, UserLoginResource, UserLogoutResource

# 파이썬 전용 mysql connector 라이브러리
# mysql-connector-python

# 비밀번호 암호화 라이브러리
# psycopg2-binary
# passlib

# 이메일 형식이 올바른지 체크해주는 라이브러리
# email-validator

# 인증 토큰 관리 및 암호화 라이브러리
# flask-jwt-extended

app = Flask(__name__)

# JWT 환경변수 설정
app.config.from_object(Config)

# JWT 매니저 초기화
jwt = JWTManager(app)

# 로그아웃된 토큰으로 API에 요청하는 경우에는 아래의 함수가 실행된다.
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in jwt_blacklist

api = Api(app)

api.add_resource(BaseHTTPResource, '/default')

api.add_resource(RecipesResource, '/recipes')
api.add_resource(RecipesByIdResource, '/recipes/<int:recipe_id>')
api.add_resource(RecipesPublishByIdResource, '/recipes/<int:recipe_id>/publish')

api.add_resource(UserRegisterResource, '/users/register')
api.add_resource(UserLoginResource, '/users/login')
api.add_resource(UserLogoutResource, '/users/logout')

if __name__ == '__main__':
    app.run()