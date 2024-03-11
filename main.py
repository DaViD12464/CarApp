from pymongo import MongoClient
import CarApi, DestinationsController, CarController, Car
from CarApi import *
<<<<<<< HEAD
app.run()

client = MongoClient("mongodb+srv://tymoteuszbroda:Dupa123@carapi.g8eabyl.mongodb.net/?retryWrites=true&w=majority&appName=CarApi")  # Update the connection string as needed
db = client['CarApi'] 
=======

>>>>>>> f09a1730debc6eaf4b8ca389581e2b3586f70896

app.run(host='127.0.0.1',port='8000')


#temp
dcontroller = DestinationsController.DestinationsController(db)
dcontroller.add_new_destination("test")
dcontroller.add_new_destination("test2")
dcontroller.load_available_destinations()
<<<<<<< HEAD

# car1 = Car.Car(brand='alfa', model='147', year=2006, engine_vol=1.6, engine_code='12345', power=120, body='fat', doors=4, paint_color='grey', vin='123456', user_id='testid', equipment=['test', 'test2'])
=======
car1 = Car.Car(brand='alfa', model='147', year=2006, engine_vol=1.6, engine_code='12345', power=120, body='fat', doors=4, paint_color='grey', vin='123456', user_id='testid', equipment=['test', 'test2'])
>>>>>>> f09a1730debc6eaf4b8ca389581e2b3586f70896

# ccontroller = CarController.CarController(db)
# ccontroller.send_car(car1, 'Żory')