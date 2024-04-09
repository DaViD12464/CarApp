from pydantic import BaseModel
#basemodel for images
class Image(BaseModel):
    url: str
    alt: str
    title: str
    description: str