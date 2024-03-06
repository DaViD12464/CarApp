from pydantic import BaseModel

#basemodel for user
class User(BaseModel):
    def __init__(self, username, password, email, phone, id):
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.id = id
    username: str
    password: str
    email: str
    phone: str
    id: int