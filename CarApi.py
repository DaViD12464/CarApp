from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import find_dotenv,load_dotenv
from bson import ObjectId

'''setting up the dotenv environment'''
#auto find the dotenv file
dotenv_path = find_dotenv()
print(dotenv_path)
#loading entries as environment variables
load_dotenv(dotenv_path)
uri = os.getenv("uri")
sec_key = os.getenv("secret_key")
algorithm = os.getenv("algorithm")


# Create a Flask app
app = Flask(__name__)
app.debug = True
# setup database


client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
    
# Create a database and a collection
db = client['CarApi']
collection_Cars = db['Cars']
collection_Users = db['Users']


@app.route('/all_users', methods=['GET'])
def get_all_users():
    users = list(collection_Users.find())
    for user in users:
        user['_id'] = str(user['_id'])
    return jsonify(users)

    