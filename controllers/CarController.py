from CarApi import collection_Cars, app
from baseclass.Car import *
from bson import ObjectId
from flask import jsonify, request

@app.route('/')
def index():
    return 'Welcome to CarApi!'

@app.route('/all_cars', methods=['GET'])
def get_all_cars():
    cars = list(collection_Cars.find())
    for car in cars:
        car['_id'] = str(car['_id'])
    return jsonify(cars)

#Endpoint to get specific car
@app.route('/car/<car_id>', methods=['GET'])
def get_car(car_id):
    car = collection_Cars.find_one({'_id': ObjectId(car_id)})
    if car:
        car['_id'] = str(car['_id'])
        return jsonify(car)
    else:
        return jsonify({'error': 'Car not found'}), 404

@app.route('/addcar', methods=['POST'])
def add_car():
    car_data = request.get_json()
    if car_data:
        result = collection_Cars.insert_one(car_data)
        if result.inserted_id:
            return jsonify({'message': 'Car added successfully', 'car_id': str(result.inserted_id)}), 201
        else:
            return jsonify({'error': 'Failed to add car'}), 500
    else:
        return jsonify({'error': 'No car data provided'}), 400


@app.route('/car/<car_id>', methods=['PUT'])
def update_car(car_id):
    data = request.get_json()
    updated_car = collection_Cars.update_one({'_id': ObjectId(car_id)}, {'$set': data})
    if updated_car.modified_count:
        return jsonify({'message': 'Car updated successfully'})
    else:
        return jsonify({'error': 'Car not found'}), 404


@app.route('/remove_car/<car_id>', methods=['DELETE'])
def delete_car(car_id):
    delete_result = collection_Cars.delete_one({'_id': ObjectId(car_id)})
    if delete_result.deleted_count:
        return jsonify({'message': 'Car deleted successfully'})
    else:
        return jsonify({'error': 'Car not found'}), 404