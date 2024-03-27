import controllers.DestinationsController as DestinationsController
import controllers.CarController as CarController
import controllers.UsersController as Controller
import controllers.ImageController as ImageController
from CarApi import *

try:
    print("Starting api...")
    app.run(host='127.0.0.1', port=8000)
except Exception as e:
    print(f"An error occurred while running Flask app: {e}")