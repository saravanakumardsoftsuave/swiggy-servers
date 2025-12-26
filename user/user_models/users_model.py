
from pydantic import BaseModel
from typing import List
class user_model(BaseModel):
    user_name :str
    user_phone_no:int
    user_email : str
    user_password:str
    user_password_confirm:str
    user_address:str
    user_lat :float
    user_long :float
class food_items(BaseModel):
    order_id:int
    food_id:int
    quantity:int

class order_model(BaseModel):
    order_id:int
    user_id :int
    hotel_id :int 
    items:list[food_items]
    total_amount:int




class update_location_model(BaseModel):
    user_lat:float
    user_long:float