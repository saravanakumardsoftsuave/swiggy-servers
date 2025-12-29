
from pydantic import BaseModel
from typing import List,Literal
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
    food_id:int
    quantity:int

class order_model(BaseModel):
    user_id :int
    hotel_id :int 
    items:list[food_items]

class payment_status(BaseModel):
    payment_method:Literal['Online','Cash_On_Delivery']


class update_location_model(BaseModel):
    user_lat:float
    user_long:float