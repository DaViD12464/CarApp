from flask import Flask, jsonify, request, send_file
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pydantic import BaseModel
import io

# Create a Flask app
app = Flask(__name__)
app.debug = True

# setup database
uri = "mongodb+srv://dawidczernik:Formula64@carapi.g8eabyl.mongodb.net/?retryWrites=true&w=majority&appName=CarApi"
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
# Create a database and a collection
db = client['CarApi']
collection_Cars = db['Cars']

# basemodel for Car
class Car(BaseModel):
    brand: str
    model: str
    year: int
    engine_vol: float
    engine_code: str
    power: int
    body: str
    doors: int
    paint_color: str
    VIN: str
    user_id: str
    equipment: list

#basemodel for user
class User(BaseModel):
    username: str
    password: str
    email: str
    phone: str
    id: list
    
    
# Use the car_model instance to perform operations on the Car model
# For example, you can call methods like car_model.get_all_cars() or car_model.add_car()

# Example usage:

@app.route('/')
def index():
    return 'Welcome to CarApi!'

@app.route('/all_cars', methods=['GET'])
def get_all_cars():
    cars = list(collection_Cars.find())
    for car in cars:
        car['_id'] = str(car['_id'])
    return jsonify(cars)

@app.route('/car', methods=['POST']) #do zrobienia (bylo jako przykladowe)
def add_car():
    data = request.get_json()
    car = Car.model.add_car(data)
    return jsonify(car), 201


if __name__ == '__main__':
    app.run(host='127.0.0.1',port='8000')