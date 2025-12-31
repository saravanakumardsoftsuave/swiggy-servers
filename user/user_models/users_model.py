from fastapi import HTTPException,status
from pydantic import BaseModel,validator
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
    @validator('user_name')
    def validator_user_name(cls,user_name):
        if user_name.strip()=='' or user_name == 'string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid user_name')
        return user_name
    @validator('user_phone_no')
    def validation_user_phone_no(cls,user_phone_no):
        if user_phone_no == 0 or user_phone_no==''.strip() or  not(6000000000 <=user_phone_no<=9999999999):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid user_phone_no')
        return user_phone_no
    @validator('user_email')
    def validation_user_email(cls,user_email):
        if user_email.strip()=='' or user_email == 'string'or not user_email.endswith('@gmail.com'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid user_email')
        return user_email
    @validator('user_password')
    def validation_user_password(cls,user_password):
        if user_password.strip()=='' or user_password == 'string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid user_password')
        return user_password
    @validator('user_password_confirm')
    def validation_user_password_confirm(cls,user_password_confirm):
        if user_password_confirm.strip()=='' or user_password_confirm == 'string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid user_password_confirm')
        return user_password_confirm
    @validator('user_address')
    def validation_user_address(cls,user_address):
        if user_address.strip()=='' or user_address == 'string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid user_address')
        return user_address
    @validator('user_lat')
    def validation_user_lat(cls,user_lat):
        if user_lat == 0.0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid user_lat')
        return user_lat
    @validator('user_long')
    def validation_user_long(cls,user_long):
        if user_long== 0.0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid user_long')
        return user_long

class food_items(BaseModel):
    food_id:int
    quantity:int

    @validator('food_id')
    def validation_food_id(cls,food_id):
        if food_id == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid food_id')
        return food_id
    @validator('quantity')
    def validation_hotel_id(cls,quantity):
        if quantity == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid quantity')
        return quantity
class order_model(BaseModel):
    user_id :int
    hotel_id :int 
    items:list[food_items]
    @validator('hotel_id')
    def validation_hotel_id(cls,hotel_id):
        if hotel_id == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid hotel_id')
        return hotel_id
    @validator('user_id')
    def val_user_id(cls,user_id):
        if user_id == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid user_id')
        return user_id
class payment_status(BaseModel):
    payment_method:Literal['Online','Cash_On_Delivery']

    @validator('payment_method')
    def validation_user_address(cls,payment_method):
        if payment_method.strip()=='' or payment_method == 'string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid payment_method')
        return payment_method

class update_location_model(BaseModel):
    user_lat:float
    user_long:float

    @validator('user_lat')
    def _user_lat(cls,user_lat):
        if user_lat == 0.0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid user_lat')
        return user_lat
    @validator('user_long')
    def _user_long(cls,user_long):
        if user_long== 0.0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid user_long')
        return user_long
