import DestinationsController, CarController
from CarApi import *
import requests
from baseclass.Car import *

app.run(host='127.0.0.1',port='8000')
#temp
# print("Destination tests")
# dcontroller = DestinationsController.DestinationsController(db)
# dcontroller.add_new_destination("test")
# dcontroller.add_new_destination("test2")
# dcontroller.load_available_destinations()
# car1 = Car.Car(brand='alfa', model='147', year=2006, engine_vol=1.6, engine_code='12345', power=120, body='fat', doors=4, paint_color='grey', vin='123456', user_id='testid', equipment=['test', 'test2'])

# ccontroller = CarController.CarController(db)
# ccontroller.send_car(car1, 'Żory')

print('adding car now\n\n\n')
url = 'http://127.0.0.1:8000/addcar'
car_data = {
  "brand": "Toyota",
  "model": "Camry",
  "year": 2020,
  "engine_vol": 2.5,
  "engine_code": "A25A-FKS",
  "power": 203,
  "body": "sedan",
  "doors": 4,
  "paint_color": "red",
  "vin": "123456789ABCDEFG",
  "user_id": "user123",
  "equipment": ["Bluetooth", "Backup Camera", "Navigation System"]
}

response = requests.post(url, json=car_data)
print(response.json())

