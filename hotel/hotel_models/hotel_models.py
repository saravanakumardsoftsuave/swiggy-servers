
from pydantic import BaseModel

class hotel_model(BaseModel):
    hotel_name: str
    hotel_phone_no: int
    hotel_email: str
    hotel_password: str
    hotel_password_confirm: str  
    hotel_address: str
    hotel_lan: float = 0.0
    hotel_long: float = 0.0

class category_model(BaseModel):
    category_name: str
    category_description: str

class food_item_model(BaseModel):
    item_name: str
    item_description: str
    item_price: float
    category_id: int

class update_location_model(BaseModel):
    hotel_lan: float
    hotel_long: float