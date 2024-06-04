import mysql.connector
from config import Config

# mysql db에 접속
def getConnection():
    connection = mysql.connector.connect(
        host=Config.HOST,
        database=Config.DATABASE,
        user=Config.USER,
        password=Config.PASSWORD
    )
    return connection