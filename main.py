from pymongo import MongoClient
import CarApi, DestinationsController, CarController, Car

from CarApi import uri

client = MongoClient(uri)  # Update the connection string as needed
db = client['CarApi'] 
api_instance = CarApi.API()

dcontroller = DestinationsController.DestinationsController(db)
dcontroller.add_new_destination("test")
dcontroller.add_new_destination("test2")
dcontroller.load_available_destinations()

car1 = Car.Car(brand='alfa', model='147', year=2006, engine_vol=1.6, engine_code='12345', power=120, body='fat', doors=4, paint_color='grey', vin='123456', user_id='testid', equipment=['test', 'test2'])

ccontroller = CarController.CarController(db)
ccontroller.send_car(car1, 'Żory')