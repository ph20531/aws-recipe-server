from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from mysql_connection import getConnection
from mysql.connector import Error
from utils import toISOFormat

# ______________________________________________________________________________________
# 인증 토큰 | 클라이언트 > 서버 | get_jwt_identity()
# ______________________________________________________________________________________

# @jwt_required()
# JWT access token이 헤더에 있어야만 실행 가능
# 따라서 로그인한 유저만 사용가능한 API

# Headers 설정
# Key   | Authorization
# Value | Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9

# get_jwt_identity()
    # Headers를 통해 입력된 access token을 복호화하여 원래의 값을 리턴

class RecipesResource(Resource):
    @jwt_required()
    def post(self):
        # - body
        data = request.get_json()

        # - headers
        user_id = get_jwt_identity()

        # - database
        try:
            connection = getConnection()

            query = '''INSERT INTO recipe (user_id, name, description, num_of_servings, cook_time, directions) VALUES (%s, %s, %s, %s, %s, %s);'''
            args = (user_id, data['name'], data['description'], data['num_of_servings'], data['cook_time'], data['directions'])

            cursor = connection.cursor()

            cursor.execute(query, args)
            connection.commit()

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
        
        # SUCCESS | 200
        return {
            'result':'success'
            }, 200
    
    @jwt_required()
    def get(self):
        # - params
        data = request.args
        offset = data['offset']
        limit = data['limit']

        # - headers
        user_id = get_jwt_identity()
        
        try:
            connection = getConnection()

            query = f'''SELECT * FROM recipe WHERE user_id = {user_id} LIMIT {offset}, {limit};'''

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query)
            result = cursor.fetchall()
            result = toISOFormat(result, 'created_at', 'updated_at')

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
        
        # SUCCESS | 200
        return {
            'result':'success',
            'items':result,
            'count':len(result)
            }, 200

class RecipesByIdResource(Resource):
    @jwt_required()
    def get(self, recipe_id):
        # - headers
        user_id = get_jwt_identity()

        try:
            connection = getConnection()

            query = f'''SELECT * FROM recipe WHERE id = {recipe_id};'''

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query)
            result = cursor.fetchall()
            result = toISOFormat(result, 'created_at', 'updated_at')

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
            # ERROR | 500
            return {
                'result':'fail',
                'error':'This item does not exist.'
                }, 500
        
        if user_id != result[0]['user_id']:
            # ERROR | 400
            return {
                'result':'fail',
                'error':'400 Bad Request. The user ID does not match the owner of the recipe.'
                }, 400
        
        # SUCCESS | 200
        return {
            'result':'success',
            'items':result,
            'count':len(result)
            }, 200
    
    @jwt_required()
    def put(self, recipe_id):
        # - body
        data = request.get_json()

        # - headers
        user_id = get_jwt_identity()

        # - database
        try:
            connection = getConnection()

            cursor = connection.cursor(dictionary=True)

            query = f'''SELECT user_id FROM recipe WHERE id = {recipe_id};'''
            cursor.execute(query)
            result = cursor.fetchone()
            print(result)

            if not result:
                cursor.close()
                connection.close()
                return {
                    'result': 'fail',
                    'error': '400 Bad Request. The recipe does not exist.'
                    }, 400

            if user_id != result['user_id']:
                cursor.close()
                connection.close()
                return {
                    'result': 'fail',
                    'error': '400 Bad Request. The user ID does not match the owner of the recipe.'
                    }, 400

            query = '''UPDATE recipe SET '''
            args = []
            for key, value in data.items():
                query += f"{key} = %s, "
                args.append(value)

            query = query[:-2] + f" WHERE id = %s;"
            args.append(recipe_id)

            cursor.execute(query, tuple(args))
            connection.commit()

            cursor.close()
            connection.close()
        except Error as e:
            if cursor is not None:
                cursor.close()

            if connection is not None:
                connection.close()

            # ERROR | 500
            return {
                'result': 'fail',
                'error': str(e)
                }, 500
        
        # SUCCESS | 200
        return {
            'result': 'success'
            }, 200
    
    @jwt_required()
    def delete(self, recipe_id):
        # - headers
        user_id = get_jwt_identity()

        try:
            connection = getConnection()

            cursor = connection.cursor(dictionary=True)

            query = f'''SELECT user_id FROM recipe WHERE id = {recipe_id};'''
            cursor.execute(query)
            result = cursor.fetchone()
            print(result)

            if not result:
                cursor.close()
                connection.close()
                return {
                    'result': 'fail',
                    'error': '400 Bad Request. The recipe does not exist.'
                    }, 400

            if user_id != result['user_id']:
                cursor.close()
                connection.close()
                return {
                    'result': 'fail',
                    'error': '400 Bad Request. The user ID does not match the owner of the recipe.'
                    }, 400

            query = f'''DELETE FROM recipe WHERE id = {recipe_id};'''

            cursor.execute(query)
            connection.commit()

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
        
        # SUCCESS | 200
        return {
            'result':'success'
            }, 200

class RecipesPublishByIdResource(Resource):
    @jwt_required()
    def post(self, recipe_id):
        # - headers
        user_id = get_jwt_identity()

        try:
            connection = getConnection()

            cursor = connection.cursor(dictionary=True)

            query = f'''SELECT user_id FROM recipe WHERE id = {recipe_id};'''
            cursor.execute(query)
            result = cursor.fetchone()
            print(result)

            if not result:
                cursor.close()
                connection.close()
                return {
                    'result': 'fail',
                    'error': '400 Bad Request. The recipe does not exist.'
                    }, 400

            if user_id != result['user_id']:
                cursor.close()
                connection.close()
                return {
                    'result': 'fail',
                    'error': '400 Bad Request. The user ID does not match the owner of the recipe.'
                    }, 400

            query = f'''UPDATE recipe SET is_publish = True WHERE id = {recipe_id};'''

            cursor.execute(query)
            connection.commit()

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
        
        # SUCCESS | 200
        return {
            'result':'success'
            }, 200
    
    @jwt_required()
    def put(self, recipe_id):
        # - headers
        user_id = get_jwt_identity()

        try:
            connection = getConnection()

            cursor = connection.cursor(dictionary=True)

            query = f'''SELECT user_id FROM recipe WHERE id = {recipe_id};'''
            cursor.execute(query)
            result = cursor.fetchone()
            print(result)

            if not result:
                cursor.close()
                connection.close()
                return {
                    'result': 'fail',
                    'error': '400 Bad Request. The recipe does not exist.'
                    }, 400

            if user_id != result['user_id']:
                cursor.close()
                connection.close()
                return {
                    'result': 'fail',
                    'error': '400 Bad Request. The user ID does not match the owner of the recipe.'
                    }, 400

            query = f'''UPDATE recipe SET is_publish = NOT is_publish WHERE id = {recipe_id};'''

            cursor.execute(query)
            connection.commit()

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
        
        # SUCCESS | 200
        return {
            'result':'success'
            }, 200

    @jwt_required()
    def delete(self, recipe_id):
        # - headers
        user_id = get_jwt_identity()

        try:
            connection = getConnection()

            cursor = connection.cursor(dictionary=True)

            query = f'''SELECT user_id FROM recipe WHERE id = {recipe_id};'''
            cursor.execute(query)
            result = cursor.fetchone()
            print(result)

            if not result:
                cursor.close()
                connection.close()
                return {
                    'result': 'fail',
                    'error': '400 Bad Request. The recipe does not exist.'
                    }, 400

            if user_id != result['user_id']:
                cursor.close()
                connection.close()
                return {
                    'result': 'fail',
                    'error': '400 Bad Request. The user ID does not match the owner of the recipe.'
                    }, 400

            query = f'''UPDATE recipe SET is_publish = False WHERE id = {recipe_id};'''

            cursor.execute(query)
            connection.commit()

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
        
        # SUCCESS | 200
        return {
            'result':'success'
            }, 200