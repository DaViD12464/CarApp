from pydantic import BaseModel
#basemodel for user
class User(BaseModel):
    username: str
    password: str
    email: str
    phone: str
    id: int