from pydantic import BaseModel
#basemodel for destinations
class Destination(BaseModel):
    street: str
    city: str
    zip_code: str
    country: str