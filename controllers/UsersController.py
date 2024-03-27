from CarApi import collection_Users, app, db, sec_key, algorithm
from baseclass.User import *
import datetime, jwt
from passlib.hash import pbkdf2_sha256
from flask import jsonify, request, make_response
from bson import ObjectId, uuid

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
    
##################################################

class User:   
    
    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=0, seconds=600),
                'iat': datetime.datetime.now(datetime.UTC),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                sec_key,
                algorithm
            )
        except Exception as e:
            return e
        
    @staticmethod   #:param auth_token:   :return: integer|string
    def decode_auth_token(auth_token): 
        try:
            payload = jwt.decode(auth_token, sec_key, algorithm)
            user_id = uuid.UUID(payload['sub'])  # Konwersja identyfikatora na obiekt UUID
            return user_id
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please try again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
        except ValueError:
            return 'Invalid UUID format.'

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
            if not (first_name and second_name and username and password and email and phone):
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
            auth_token = User.encode_auth_token(self,user['_id'])

            #password encryption
            user['password'] = pbkdf2_sha256.encrypt(user['password'])

            #check for existing email adress or phone number
            if db.Users.find_one({"email":  user['email'] }):
                responseObject = {
                'status': 'fail',
                'message': 'User with this Email address already exists.',
            }
                return make_response(jsonify(responseObject)), 400
            if db.Users.find_one({"phone":  user['phone'] }):
                responseObject = {
                'status': 'fail',
                'message': 'User with this phone number already exists.',
            }
                return make_response(jsonify(responseObject)), 400
            if db.Users.find_one({"username":  user['username'] }):
                responseObject = {
                'status': 'fail',
                'message': 'User with this username already exists.',
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
  
    
    def login(self):
        try:
            # Extracting form data
            data = request.json
            usernameOrMail = data.get('usernameOrMail')
            password = data.get('password')
            if not (usernameOrMail and password):
                return make_response(jsonify("Missing one of required fields.")), 400
            user = db.Users.find_one({'$or': [{'username': usernameOrMail}, {'email': usernameOrMail}]})
            if user and pbkdf2_sha256.verify(password, user['password']):
                auth_token = User.encode_auth_token(self,user['_id'])
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token
                }
                return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Invalid username/email or password.'
                }
                return make_response(jsonify(responseObject)), 401
        except Exception as e:
            print(e)
  
    def logout(self):
        try:
            auth_token = request.headers.get('Authorization')
            if auth_token:
                user_id = User.decode_auth_token(auth_token)
                if isinstance(user_id, str):
                    responseObject = {
                        'status': 'fail',
                        'message': user_id
                    }
                    return make_response(jsonify(responseObject)), 401
                else:
                    # Tutaj usuń lub oznacz token jako nieważny
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged out.'
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Provide a valid auth token.'
                }
                return make_response(jsonify(responseObject)), 403
        except Exception as e:
            print(e)
    
    def delete_user(self):
        try:
            user_id = request.json.get('id')
            result = db.Users.delete_one({'_id': user_id})
            if result.deleted_count == 1:
                response = {'message': f'User with ID {user_id} deleted successfully'}
                return jsonify(response), 200
            else:
                response = {'message': f'User with ID {user_id} not found'}
                return jsonify(response), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
# Routes for User class    
@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()


@app.route('/user/login', methods=['POST'])
def login():
    return User().login()

@app.route('/user/logout', methods=['GET'])
def logout():
    return User().logout()

@app.route('/user/deleteAccount', methods=['DELETE'])
def delete_user():
    return User().delete_user()