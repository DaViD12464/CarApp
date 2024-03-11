from CarApi import *
from baseclass import *
from baseclass.Car import Car  #not used ---
from baseclass.User import User #not used ---
from pymongo.collection import Collection
from pymongo.database import Database


class DestinationsController:
    #add new values here and then call load_available_destinations() in main file to add content of this list to database, add_new_destination() method also works
    available_destinations = []
    
    def __init__(self, db: Database):
        self.cars_collection: Collection = db['Cars']
        self.available_destinations_collection: Collection = db['Available_destinations']
        
    def load_available_destinations(self):
        for destination in self.available_destinations:
            self.available_destinations_collection.insert_one({'name': destination})

    def add_new_destination(self, destination: str):
        #cannot iterate over Collection, next 2 lines are for making this possible.
        destination_names = self.list_available_destinations()
        
        if destination not in destination_names:
            self.available_destinations_collection.insert_one({'name': destination})
            self.available_destinations.append(destination)
        else:
            print(f"{destination} is already on company's Cities list")
            
    def list_available_destinations(self):
        destinations = self.available_destinations_collection.find({})
        return [name['name'] for name in destinations]