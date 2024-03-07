from CarApi import Car
from Car import Car
from User import User
from pymongo.collection import Collection
from pymongo.database import Database


class Controller:
    available_destinations = ['Warsaw', 'Berlin', 'Liepzig', 'Bochum', 'Gliwice', 'Hamburg', 'Milan', 'Riga', 'Madrid', 'Paris', 'Żory', 'Vienna', 'Katowice', 'Prague']
    
    def __init__(self, db: Database):
        self.available_destinations_collection: Collection = db['Available_destinations']
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
        
    # def add_new_destination(self, destination: str):
    #     if destination not in self.available_destinations_collection['name']:
    #         self.available_destinations_collection.insert_one({'name': destination})
    #         self.available_destinations.append(destination)
    #     else:
    #         print("{destination} is already on company's Cities list")