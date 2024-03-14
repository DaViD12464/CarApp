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
    def __init__(self, brand, model, year, engine_vol, engine_code, power, body, doors, paint_color, vin, user_id, equipment):
        self.brand = brand
        self.model = model
        self.year = year
        self.engine_vol = engine_vol
        self.engine_code = engine_code
        self.power = power
        self.body = body
        self.doors = doors
        self.paint_color = paint_color
        self.vin = vin
        self.user_id = user_id
        self.equipment = equipment
