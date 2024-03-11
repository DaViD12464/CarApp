import DestinationsController, CarController
from CarApi import *

from baseclass import *

app.run(host='127.0.0.1',port='8000')


#temp
dcontroller = DestinationsController.DestinationsController(db)
dcontroller.add_new_destination("test")
dcontroller.add_new_destination("test2")
dcontroller.load_available_destinations()
car1 = Car.Car(brand='alfa', model='147', year=2006, engine_vol=1.6, engine_code='12345', power=120, body='fat', doors=4, paint_color='grey', vin='123456', user_id='testid', equipment=['test', 'test2'])

ccontroller = CarController.CarController(db)
ccontroller.send_car(car1, 'Żory')