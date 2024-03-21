import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from CarApi import * # Załóżmy, że "app" to nazwa twojego pliku z aplikacją Flask

'''setting up the dotenv environment'''
#auto find the dotenv file
dotenv_path = find_dotenv()
print(dotenv_path)
#loading entries as environment variables
load_dotenv(dotenv_path)
uri = os.getenv("uri")

# Create a Flask app
app = Flask(__name__)
app.debug = True
# setup database


client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
    
# Create a database and a collection
db = client['CarApi']
collection_Cars = db['Cars']
collection_Users = db['Users']

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_all_users(client):
    """Testowanie endpointu /all_users"""
    rv = client.get('/all_users')
    assert rv.status_code == 200
    assert isinstance(rv.json, list)  # Sprawdzenie, czy odpowiedź jest listą