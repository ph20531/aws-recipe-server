from flask_restful import Resource

# Basics ________________________________________________________________________________
# CREATE | POST
# READ   | GET
# UPDATE | PUT
# DELETE | DELETE

# Inputs ________________________________________________________________________________
# URL
# - URL은 Argument로 사용

# Body
# - body는 POST, PUT, PATCH에 사용
# - data = request.get_json()

# Params
# - params는 GET에 사용
# - data = request.args

# Headers
# - Headers는 인증 토큰에 사용 

# Execute _______________________________________________________________________________
# GET, DELETE
# - cursor.execute(query)

# POST, PUT
# - cursor.execute(query, args)

# 인증 토큰(auth token) __________________________________________________________________
# 사용자마다 회원가입 및 로그인 시 user_id를 이용하여 access_token을 발급해준다.
# access_token을 발급받은 사용자는 서비스를 이용할 수 있다.

# 개발 프로세스
# 서버 > 클라이언트
# - 사용자마다 회원가입 및 로그인 시 user_id를 이용하여 access_token을 발급

# 클라이언트 > 서버
# - 발급받은 access_token을 Headers을 통해 넘겨주면 해당 서비스 api의 user_id와 비교하여 서비스 이용
# - Headers 설정
# Key   | Authorization
# Value | Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9

# 주로 사용되는 HTTP 응답 코드 ____________________________________________________________
# 200 OK: 요청이 성공적으로 처리되었음을 나타냅니다.
# 201 Created: 요청이 성공적으로 처리되었고, 새로운 리소스가 생성되었음을 나타냅니다.
# 204 No Content: 요청이 성공적으로 처리되었지만 응답에 본문이 없음을 나타냅니다.
# 400 Bad Request: 요청이 잘못되었거나 서버가 이해할 수 없는 형식일 경우에 사용됩니다.
# 401 Unauthorized: 요청이 인증되지 않았거나 인증 정보가 유효하지 않을 경우에 사용됩니다.
# 403 Forbidden: 요청이 서버에 의해 거부되었음을 나타냅니다.
# 404 Not Found: 요청된 리소스가 서버에 없음을 나타냅니다.
# 500 Internal Server Error: 서버 측에서 예기치 않은 오류가 발생했음을 나타냅니다.
# 503 Service Unavailable: 서버가 현재 사용할 수 없음을 나타냅니다.

# 대표적인 3가지 HTTP 응답 코드 ____________________________________________________________
# 200 OK: 요청이 성공적으로 처리되었음을 나타냅니다.
# 400 Bad Request: 요청이 잘못되었거나 서버가 이해할 수 없는 형식일 경우에 사용됩니다.
# 500 Internal Server Error: 서버 측에서 예기치 않은 오류가 발생했음을 나타냅니다.

class BaseHTTPResource(Resource):
    def post(self):
        return {
            'data':'CREATE | POST'
            }

    def get(self):
        return {
            'data':'READ | GET'
            }
    
    def put(self):
        return {
            'data':'UPDATE | PUT'
            }
    
    def delete(self):
        return {
            'data':'DELETE | DELETE'
            }