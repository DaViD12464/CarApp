from pymongo import MongoClient
import CarApi, DestinationsController, CarController, Car
from CarApi import *

app.run(host='127.0.0.1',port='8000')


#temp
dcontroller = DestinationsController.DestinationsController(db)
dcontroller.add_new_destination("test")
dcontroller.add_new_destination("test2")
dcontroller.load_available_destinations()