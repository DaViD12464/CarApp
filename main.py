import controllers.DestinationsController as DestinationsController, controllers.CarController as CarController, controllers.UsersController as Controller # --not used
from CarApi import *

try:
    app.run(host='0.0.0.0', port=8000)
except Exception as e:
    print(f"An error occurred while running Flask app: {e}")