
from pydantic import BaseModel,Field,validator,EmailStr
from fastapi import HTTPException,status
from typing import Literal
class drive_model(BaseModel):
    driver_name: str
    driver_bike_no: str
    driver_license_no: str
    driver_phone_no: int
    driver_email: EmailStr
    driver_password: str
    driver_password_confirm: str  
    driver_address: str
    driver_lat: float = 0.0
    driver_long: float = 0.0

    @validator('driver_name')
    def validator_driver_name(cls,driver_name):
        if driver_name.strip()=='' or driver_name == 'string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid driver_name')
        return driver_name
    
    @validator('driver_phone_no')
    def validation_driver_phone_no(cls,driver_phone_no):
        if driver_phone_no == 0 or driver_phone_no==''.strip() or not(6000000000 <=driver_phone_no<=9999999999):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid driver_phone_no')
        return driver_phone_no
    @validator('driver_bike_no')
    def validation_driver_bike_no(cls,driver_bike_no):
        if driver_bike_no.strip()=='' or driver_bike_no == 'string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid driver_bike_no')
        return driver_bike_no
    @validator('driver_license_no')
    def validation_driver_license_no(cls,driver_license_no):
        if driver_license_no.strip()=='' or driver_license_no == 'string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid driver_license_no')
        return driver_license_no
    @validator('driver_email')
    def validation_driver_email(cls,driver_email):
        if driver_email.strip()=='' or driver_email == 'string' or not driver_email.endswith('@gmail.com'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid driver_email')
        return driver_email
    @validator('driver_password')
    def validation_driver_password(cls,driver_password):
        if driver_password.strip()=='' or driver_password == 'string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid driver_password')
        return driver_password
    @validator('driver_password_confirm')
    def validation_driver_password_confirm(cls,driver_password_confirm):
        if driver_password_confirm.strip()=='' or driver_password_confirm == 'string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid driver_password_confirm')
        return driver_password_confirm
    @validator('driver_address')
    def validation_driver_address(cls,driver_address):
        if driver_address.strip()=='' or driver_address == 'string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid driver_address')
        return driver_address
    @validator('driver_lat')
    def validation_driver_lat(cls,driver_lat):
        if driver_lat == 0.0 or  not (-90 <= driver_lat <= 90):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid driver_lat')
        return driver_lat
    @validator('driver_long')
    def validation_driver_long(cls,driver_long):
        if driver_long== 0.0 or  not (-180 <= driver_long <= 180):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid driver_long')
        return driver_long
    


class update_location_model(BaseModel):
    driver_lat: float
    driver_long: float
    @validator('driver_lat')
    def _driver_lat(cls,driver_lat):
        if driver_lat == 0.0 or not (-90 <= driver_lat <= 90):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid driver_lat')
        return driver_lat
    @validator('driver_long')
    def _driver_long(cls,driver_long):
        if driver_long== 0.0 or not (-180 <= driver_long <= 180):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid driver_long')
        return driver_long
class orderrequest(BaseModel):
    response:Literal['Accept','reject']
    order_id:int
    hotel_id:int
    user_id:int

    @validator('response')
    def validation_response(cls,response):
        if response.strip()=='' or response == 'string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid response')
        return response
    @validator('order_id')
    def validation_order_id(cls,order_id):
        if order_id == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid order_id')
        return order_id
    @validator('hotel_id')
    def validation_hotel_id(cls,hotel_id):
        if hotel_id == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid hotel_id')
        return hotel_id
    @validator('user_id')
    def validation_user_id(cls,user_id):
        if user_id == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid user_id')
        return user_id
    
    
class update_status(BaseModel):
    order_id:int
    current_status:str=Field(...,examples=['ORDER PICKED','ON THE WAY','ORDER DELIVERIED'])
    @validator('order_id')
    def _order_id(cls,order_id):
        if order_id == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid order_id')
        return order_id
    @validator('current_status')
    def validation_response(cls,current_status):
        if current_status.strip()=='' or current_status == 'string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid current_status')
        return current_status
