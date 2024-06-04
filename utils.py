from datetime import datetime

def toISOFormat(data, *columns):
    for row in data:
        for column in columns:
            if column in row and isinstance(row[column], datetime):
                row[column] = row[column].isoformat()
    return data

def isEmpty(data, *columns):
    for column in columns:
        if column not in data or not data.get(column)\
            or (isinstance(data.get(column), str) and data.get(column).strip() == ''):
            return True
    return False

from passlib.hash import pbkdf2_sha256
from config import Config

# 단방향으로 암호화된 비밀번호 리턴
def encryption(original_password):
    return pbkdf2_sha256.hash(original_password + Config.SALT)

# 입력된 비밀번호와 해시화 된 비밀번호와 일치하는지 체크
def decryption(original_password, hashed_password):
    return pbkdf2_sha256.verify(original_password + Config.SALT, hashed_password)