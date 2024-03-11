from pydantic import BaseModel
#basemodel for destinations
class Destination(BaseModel):
    street: str
    city: str
    zip_code: str
    country: str
    def __init__(self, street, city, zip_code, country):
        self.street = street
        self.city = city
        self.zip_code = zip_code
        self.country = country