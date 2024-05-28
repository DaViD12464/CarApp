import pytest, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bson import ObjectId
from flask import json
from CarApi import collection_Cars
from pymongo import MongoClient
from main import app

@pytest.fixture        
def client():
    # Set the app to testing mode
    app.config['TESTING'] = True
    # Use database for testing
    uri = os.getenv("uri")
    # Update the app's MongoDB URI configuration
    client = MongoClient(uri)
    
    with app.test_client() as client:
        yield client

# Test for the index route
def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to CarApi!' in response.data

# Test for getting all cars
def test_get_all_cars(client, monkeypatch):
    test_cars = [
        {'_id': ObjectId(), 'name': 'Test Car 1'},
        {'_id': ObjectId(), 'name': 'Test Car 2'}
    ]
    
    def mock_find():
        return test_cars

    monkeypatch.setattr(collection_Cars, 'find', mock_find)

    response = client.get('/all_cars')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['name'] == 'Test Car 1'
    assert data[1]['name'] == 'Test Car 2'

# Test for getting a specific car
def test_get_car(client, monkeypatch):
    test_car = {'_id': ObjectId(), 'name': 'Test Car'}

    def mock_find_one(query):
        if query['_id'] == test_car['_id']:
            return test_car
        return None

    monkeypatch.setattr(collection_Cars, 'find_one', mock_find_one)

    response = client.get(f'/car/{test_car["_id"]}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Test Car'

    response = client.get('/car/000000000000000000000000')
    assert response.status_code == 404

# Test for adding a car
def test_add_car(client, monkeypatch):
    def mock_insert_one(data):
        return type('obj', (object,), {'inserted_id': ObjectId()})()

    monkeypatch.setattr(collection_Cars, 'insert_one', mock_insert_one)

    response = client.post('/addcar', json={'name': 'New Car'})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'car_id' in data

    response = client.post('/addcar', json={})
    assert response.status_code == 400

# Test for updating a car
def test_update_car(client, monkeypatch):
    def mock_update_one(query, update):
        if query['_id'] == ObjectId('60c72b2f4f1a4e3d3f4d4a4b'):
            return type('obj', (object,), {'modified_count': 1})()
        return type('obj', (object,), {'modified_count': 0})()

    monkeypatch.setattr(collection_Cars, 'update_one', mock_update_one)

    response = client.put('/car/60c72b2f4f1a4e3d3f4d4a4b', json={'name': 'Updated Car'})
    assert response.status_code == 200

    response = client.put('/car/000000000000000000000000', json={'name': 'Updated Car'})
    assert response.status_code == 404

# Test for deleting a car
def test_delete_car(client, monkeypatch):
    def mock_delete_one(query):
        if query['_id'] == ObjectId('60c72b2f4f1a4e3d3f4d4a4b'):
            return type('obj', (object,), {'deleted_count': 1})()
        return type('obj', (object,), {'deleted_count': 0})()

    monkeypatch.setattr(collection_Cars, 'delete_one', mock_delete_one)

    response = client.delete('/remove_car/60c72b2f4f1a4e3d3f4d4a4b')
    assert response.status_code == 200

    response = client.delete('/remove_car/000000000000000000000000')
    assert response.status_code == 404
