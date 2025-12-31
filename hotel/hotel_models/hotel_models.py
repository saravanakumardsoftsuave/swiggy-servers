from fastapi import HTTPException,status
from pydantic import BaseModel,validator
from typing import List,Literal
class hotel_model(BaseModel):
    hotel_name: str
    hotel_phone_no: int
    hotel_email: str
    hotel_password: str
    hotel_password_confirm: str  
    hotel_address: str
    hotel_lat: float = 0.0
    hotel_long: float = 0.0

    @validator('hotel_name')
    def validator_hotel_name(cls,hotel_name):
        if hotel_name.strip()=='' or hotel_name == 'string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid hotel_name')
        return hotel_name
    @validator('hotel_phone_no')
    def validation_driver_phone_no(cls,hotel_phone_no):
        if hotel_phone_no == 0 or hotel_phone_no==''.strip() or not(6000000000 <=hotel_phone_no<=9999999999):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid hotel_phone_no')
        return hotel_phone_no
    @validator('hotel_email')
    def validation_hotel_email(cls,hotel_email):
        if hotel_email.strip()=='' or hotel_email == 'string' or not hotel_email.endswith('@gmail.com'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid hotel_email')
        return hotel_email
    @validator('hotel_password')
    def validation_hotel_password(cls,hotel_password):
        if hotel_password.strip()=='' or hotel_password == 'string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid hotel_password')
        return hotel_password
    @validator('hotel_password_confirm')
    def validation_hotel_password_confirm(cls,hotel_password_confirm):
        if hotel_password_confirm.strip()=='' or hotel_password_confirm == 'string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid hotel_password_confirm')
        return hotel_password_confirm
    @validator('hotel_address')
    def validation_hotel_address(cls,hotel_address):
        if hotel_address.strip()=='' or hotel_address == 'string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid hotel_address')
        return hotel_address
    @validator('hotel_lat')
    def validation_hotel_lat(cls,hotel_lat):
        if hotel_lat == 0.0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid hotel_lat')
        return hotel_lat
    @validator('hotel_long')
    def validation_hotel_long(cls,hotel_long):
        if hotel_long== 0.0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid hotel_long')
        return hotel_long
class category_model(BaseModel):
    hotel_id:int
    category_name: str
    category_description: str
    @validator('hotel_id')
    def validation_hotel_id(cls,hotel_id):
        if hotel_id == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid hotel_id')
        return hotel_id
    @validator('category_name')
    def validation_category_name(cls,category_name):
        if category_name.strip()=='' or category_name == 'string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid category_name')
        return category_name
    @validator('category_description')
    def validation_hotel_address(cls,category_description):
        if category_description.strip()=='' or category_description == 'string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid category_description')
        return category_description

class food_item_model(BaseModel):
    category_id:int
    item_name: str
    item_description: str
    item_price: float
    @validator('category_id')
    def validation_category_id(cls,category_id):
        if category_id == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid category_id')
        return category_id
    @validator('item_name')
    def validation_item_name(cls,item_name):
        if item_name.strip()=='' or item_name == 'string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid item_name')
        return item_name
    @validator('item_description')
    def validation_item_description(cls,item_description):
        if item_description.strip()=='' or item_description == 'string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid item_description')
        return item_description
    @validator('item_price')
    def validation_driver_lat(cls,item_price):
        if item_price == 0.0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid item_price')
        return item_price
    
class update_location_model(BaseModel):
    hotel_lat: float
    hotel_long: float
    @validator('hotel_lat')
    def _hotel_lat(cls,hotel_lat):
        if hotel_lat == 0.0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid hotel_lat')
        return hotel_lat
    @validator('hotel_long')
    def _hotel_long(cls,hotel_long):
        if hotel_long== 0.0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid hotel_long')
        return hotel_long

class Orderrequest(BaseModel):
    order_id:int
    response:Literal['accept','reject']

    @validator('order_id')
    def _order_id(cls,order_id):
        if order_id == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid order_id')
        return order_id
    @validator('response')
    def validation_response(cls,response):
        if response.strip()=='' or response == 'string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid response')
        return response
    