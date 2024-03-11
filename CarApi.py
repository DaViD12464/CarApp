from flask import Flask, jsonify, request, send_file
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from Car import *
import os
from dotenv import find_dotenv,load_dotenv

'''setting up the dotenv environment'''
#auto find the dotenv file
dotenv_path = find_dotenv()
print(dotenv_path)
#loading entries as environment variables
load_dotenv(dotenv_path)
uri = os.getenv("uri")

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

@app.route('/')
def index():
    return 'Welcome to CarApi!'
@app.route('/all_cars', methods=['GET'])
def get_all_cars():
    cars = list(collection_Cars.find())
    for car in cars:
        car['_id'] = str(car['_id'])
    return jsonify(cars)
@app.route('/addcar', methods=['POST'])
def add_car():
    data = request.get_json()
    car = Car.model.add_car(data)
    return jsonify(car), 201
if __name__ == '__main__':
    app.run(host='127.0.0.1',port='8000')