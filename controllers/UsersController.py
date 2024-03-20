from CarApi import collection_Users, app, db, sec_key
from baseclass.User import *
import uuid, datetime, jwt
from passlib.hash import pbkdf2_sha256
from flask import jsonify, request, make_response
from bson import ObjectId

@app.route('/all_users', methods=['GET'])
def get_all_users():
    users = list(collection_Users.find())
    for user in users:
        user['_id'] = str(user['_id'])
    return jsonify(users)

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = collection_Users.find_one({'_id': ObjectId(user_id)})
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404


#probably unusefull - can change it to an admin option to link user with his company/organization
@app.route('/adduser', methods=['POST'])
def add_user():
    user_data = request.get_json()
    if user_data:
        result = collection_Users.insert_one(user_data)
        if result.inserted_id:
            return jsonify({'message': 'User added successfully', 'user_id': str(result.inserted_id)}), 201
        else:
            return jsonify({'error': 'Failed to add user'}), 500
    else:
        return jsonify({'error': 'No user data provided'}), 400

@app.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    updated_user = collection_Users.update_one({'_id': ObjectId(user_id)}, {'$set': data})
    if updated_user.modified_count:
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/delete_user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    delete_result = collection_Users.delete_one({'_id': ObjectId(user_id)})
    if delete_result.deleted_count:
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404
    
##################################################
# Używane do rejestracji i logowania z autoryzacja tokenem:
# https://realpython.com/token-based-authentication-with-flask/#register-route
# https://github.com/realpython/flask-jwt-auth/blob/master/project/server/models.py

class User:   
    
    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.now(datetime.UTC),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                sec_key,
                algorithm='HS256'
            )
        except Exception as e:
            return e
        
    @staticmethod   #:param auth_token:   :return: integer|string
    def decode_auth_token(auth_token): 
        try:
            payload = jwt.decode(auth_token, sec_key)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please try again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def signup(self):
        try:
            # Extracting form data
            data = request.json

            first_name = data.get('first_name')
            second_name = data.get('second_name')
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            phone = data.get('phone')
            

            # Validation of data
            if not ("first_name" and "second_name" and "username" and "password" and "email" and "phone"):
                return make_response(jsonify("Missing one of required fields.")), 400
            #creation of user object
            user = {
                "_id": uuid.uuid4().hex,
                "first_name": first_name,
                "second_name": second_name,
                "username": username,
                "password": password,
                "email": email,
                "phone": phone,
                "user_privileges": "basicUser", 
            }
            #generate auth token
            auth_token = User.encode_auth_token(user,user['_id'])

            #password encryption
            user['password'] = pbkdf2_sha256.encrypt(user['password'])

            #check for existing email adress or phone number
            if db.Users.find_one({"email":  user['email'] }):
                responseObject = {
                'status': 'fail',
                'message': 'Username with this Email address already exists.',
            }
                return make_response(jsonify(responseObject)), 400
            if db.Users.find_one({"phone":  user['phone'] }):
                responseObject = {
                'status': 'fail',
                'message': 'Username with this phone number already exists.',
            }
                return make_response(jsonify(responseObject)), 400
            responseObject = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token
                }
            if db.Users.insert_one(user):
                return make_response(jsonify(responseObject)), 201                                   

        except Exception as e:  
            print(e) # Print exception for debugging 
            responseObject = {
                'status': 'fail',
                'message': 'Internal server error.',
            }
            return make_response(jsonify(responseObject)), 500
  
        
# Routes for User class    
@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()
'''
@app.route('/user/login', methods=['POST'])
def login():
    return User().login()

@app.route('/user/logout', methods=['GET'])
def logout():
    return User().logout()
'''