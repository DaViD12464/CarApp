from CarApi import *
from Car import Car
from User import User
from pymongo.collection import Collection
from pymongo.database import Database


class Controller:
    #add new values here and then call load_available_destinations() in main file to add content of this list to database, add_new_destination() method also works
    available_destinations = []
    
    def __init__(self, db: Database, table:str):
        self.available_destinations_collection: Collection = db[table]
        self.load_available_destinations()
        
    def load_available_destinations(self):
        for destination in self.available_destinations:
            self.available_destinations_collection.insert_one({'name': destination})
    
    def assign_car_to_user(self, Car, User):
        pass
    
    def send_car(self, car:Car, destination:str):
        if destination in self.available_destinations:
            return f"sending {car.brand} to {destination}"
        else: 
            return f"{destination} is not on the company's Cities list"
        
    def add_car_to_fleet(self, car:Car):
        pass
               
    def add_new_destination(self, destination: str):
        #cannot iterate over Collection, next 2 lines are for making this possible.
        destinations = self.available_destinations_collection.find({})
        destination_names = [name['name'] for name in destinations]
        
        if destination not in destination_names:
            self.available_destinations_collection.insert_one({'name': destination})
            self.available_destinations.append(destination)
        else:
            print(f"{destination} is already on company's Cities list")