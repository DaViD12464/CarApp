from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import find_dotenv,load_dotenv


'''setting up the dotenv environment'''
#auto find the dotenv file
dotenv_path = find_dotenv()
print(dotenv_path)
#loading entries as environment variables
load_dotenv(dotenv_path)
uri = os.getenv("uri")
sec_key = os.getenv("secret_key")
algorithm = os.getenv("algorithm")
image_path = os.getenv("basePhotoPath")

# Create a Flask app
app = Flask(__name__)
app.debug = False
# setup database


client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
    
# Create a database and a collection
db = client.CarApi
collection_Cars = db['Cars']
collection_Users = db['Users']

try:
    print("Starting api...")
    app.run(host='0.0.0.0', port=5000)
except Exception as e:
    print(f"An error occurred while running Flask app: {e}")