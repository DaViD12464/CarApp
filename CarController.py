from CarApi import *
from Car import Car
from User import User
from pymongo.collection import Collection
from pymongo.database import Database


class CarController:
    
    def __init__(self, db: Database):
        self.cars_collection: Collection = db['Cars']
        self.available_destinations_collection: Collection = db['Available_destinations']
        
    def send_car(self, car:Car, destination:str):
        cars_collection = self.list_cars()
        if car not in cars_collection:
            print(f'{car.brand} is not part of the fleet')
            return 0
        if destination not in self.available_destinations_collection:
            print(f"{destination} is not on the company's Cities list")
            return 0
        if car in cars_collection and destination in self.available_destinations_collection:
            print(f"sending {car.brand} to {destination}")

    def list_cars(self):
        cars = self.cars_collection.find({})
        return [name['brand'] for name in cars]