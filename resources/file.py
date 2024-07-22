from flask import request, jsonify, send_from_directory, url_for
import os
from werkzeug.utils import secure_filename
from flask_restful import Resource
import boto3
from botocore.exceptions import ClientError
# 사용법 __________________________________________________________________________________________________________
# 001. 로컬 파일 업로드:
# 포스트맨에서 POST 요청을 보낼 때
# URL에 http://localhost:5000/upload/local을 입력하고
# Body 탭에서 form-data로 파일을 첨부합니다.
# 파일을 업로드할 때에는 file이라는 키를 사용하여 파일을 첨부해야 합니다.

# 002. 로컬 파일 다운로드:
# 포스트맨에서 GET 요청을 보낼 때
# URL에 http://localhost:5000/download/local/파일이름을 입력하면 해당 파일이 다운로드됩니다.
# 파일 이름은 실제 업로드된 파일의 이름으로 대체되어야 합니다.

# 003. 로컬 파일 Url 얻기:
# 포스트맨에서 GET 요청을 보낼 때
# URL에 http://localhost:5000/url/local/파일이름을 입력하면 해당 파일의 url을 얻을 수 있습니다.
# 파일 이름은 실제 업로드된 파일의 이름으로 대체되어야 합니다.

# 003. 로컬 파일 삭제:
# 포스트맨에서 DELETE 요청을 보낼 때
# URL에 http://localhost:5000/delete/local/파일이름을 입력하면 해당 파일이 삭제됩니다.
# 파일 이름은 실제 업로드된 파일의 이름으로 대체되어야 합니다.

# Common Settings __________________________________________________________________________________________________________
# 전역 변수로 파일 크기 제한 설정 (10MB로 설정)
FILE_SIZE_LIMIT = 10 * 1024 * 1024  # 10MB

# Localhost File System __________________________________________________________________________________________________________
# 로컬 파일 디렉토리 설정
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

class LocalFileUpload(Resource):
    def post(self):
        if 'file' not in request.files:
            return {'error': 'No file part'}, 400
        
        files = request.files.getlist('file')  # 여러 파일을 받기 위해 getlist()를 사용합니다.
        
        for file in files:
            # 파일 크기 확인
            if file and file.content_length > FILE_SIZE_LIMIT:
                return {'error': 'File size exceeds limit'}, 400
            
            if file.filename == '':
                return {'error': 'No selected file'}, 400
            
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
        
        return {'message': 'Files uploaded successfully'}, 200

class LocalFileDownload(Resource):
    def get(self, filename):
        return send_from_directory(UPLOAD_FOLDER, filename)
    
class LocalFileDelete(Resource):
    def delete(self, filename):
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return {'message': 'File deleted successfully'}, 200
        else:
            return {'error': 'File not found'}, 400

# Amazon S3 File System __________________________________________________________________________________________________________
# Amazon S3 설정
S3_BUCKET_NAME = 'your-s3-bucket-name'
S3_ACCESS_KEY = 'your-s3-access-key'
S3_SECRET_KEY = 'your-s3-secret-key'

s3 = boto3.client('s3', aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY)

class S3FileUpload(Resource):
    def post(self):
        if 'file' not in request.files:
            return {'error': 'No file part'}, 400
        
        files = request.files.getlist('file')  # 여러 파일을 받기 위해 getlist()를 사용합니다.
        
        for file in files:
            # 파일 크기 확인
            if file and file.content_length > FILE_SIZE_LIMIT:
                return {'error': 'File size exceeds limit'}, 400
            
            if file.filename == '':
                return {'error': 'No selected file'}, 400
            
            try:
                s3.upload_fileobj(file, S3_BUCKET_NAME, file.filename)
            except ClientError as e:
                return {'error': e.response['Error']['Message']}, 400
        
        return {'message': 'Files uploaded successfully'}, 200

class S3FileDownload(Resource):
    def get(self, filename):
        try:
            obj = s3.get_object(Bucket=S3_BUCKET_NAME, Key=filename)
            return obj['Body'].read()
        except ClientError as e:
            return {'error': e.response['Error']['Message']}, 400
        
class S3FileDelete(Resource):
    def delete(self, filename):
        try:
            s3.delete_object(Bucket=S3_BUCKET_NAME, Key=filename)
            return {'message': 'File deleted successfully'}, 200
        except ClientError as e:
            return {'error': e.response['Error']['Message']}, 400