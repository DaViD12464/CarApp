from pydantic import BaseModel
#basemodel for user
class User(BaseModel):
    first_name: str
    second_name: str
    username: str
    password: str
    email: str
    phone: int
    user_privilleges: str