
from pydantic import BaseModel

class hotel_model(BaseModel):
    hotel_name: str
    hotel_phone_no: int
    hotel_email: str
    hotel_password: str
    hotel_password_confirm: str  
    hotel_address: str
    hotel_lat: float = 0.0
    hotel_long: float = 0.0

class category_model(BaseModel):
    hotel_id:int
    category_name: str
    category_description: str

class food_item_model(BaseModel):
    category_id:int
    item_name: str
    item_description: str
    item_price: float

class update_location_model(BaseModel):
    hotel_lat: float
    hotel_long: float