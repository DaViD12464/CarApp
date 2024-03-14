from pydantic import BaseModel
# basemodel for Car
class Car(BaseModel):
    brand: str
    model: str
    year: int
    engine_vol: float
    engine_code: str
    power: int
    body: str
    doors: int
    paint_color: str
    vin: str
    user_id: str
    equipment: list
