from pymongo import MongoClient
import CarApi, Controller 

client = MongoClient("mongodb+srv://tymoteuszbroda:Dupa123@carapi.g8eabyl.mongodb.net/?retryWrites=true&w=majority&appName=CarApi")  # Update the connection string as needed
db = client['CarApi'] 
api_instance = CarApi.API()

controller = Controller.Controller(db)
controller.add_new_destination("test")
controller.add_new_destination("test2")
controller.load_available_destinations()