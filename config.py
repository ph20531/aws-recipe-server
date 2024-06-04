# 주의 | 절대 Github에 commit하면 안됨
class Config:
    # Localhost Database ______________________________________________________________________
    HOST='127.0.0.1'
    DATABASE='recipe_db'
    USER='food'
    PASSWORD='2052'

    # AWS Database ______________________________________________________________________
    # HOST='database-1.cr0u4qkgeysk.ap-northeast-2.rds.amazonaws.com'
    # DATABASE='recipe_db'
    # USER='food'
    # PASSWORD='2052'

    # Password ______________________________________________________________________
    SALT = 'qDre72A7t1Dhebr45KFW8u7yus7d5f1Ds2KabFJ'

    # JWT ___________________________________________________________________________
    JWT_SECRET_KEY = 'Z1wY65oOb85nT956GAKdE23Tl1w2G4o3A45dBSQ'

    # False | 액세스 토큰에 대한 만료 시간이 없음
    # Integer | 초단위로 액세스 토큰의 유효 기간을 설정
    JWT_ACCESS_TOKEN_EXPIRES = False
    
    # 예외 발생 시 클라이언트에게 보낼것인지 여부
    PROPAGATE_EXCEPTIONS = True
