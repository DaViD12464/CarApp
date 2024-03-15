from CarApi import *
from baseclass.User import *

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

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    delete_result = collection_Users.delete_one({'_id': ObjectId(user_id)})
    if delete_result.deleted_count:
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404