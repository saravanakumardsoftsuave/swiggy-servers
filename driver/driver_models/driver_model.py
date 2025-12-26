
from pydantic import BaseModel

class drive_model(BaseModel):
    driver_name: str
    driver_bike_no: str
    driver_license_no: str
    driver_phone_no: int
    driver_email: str
    driver_password: str
    driver_password_confirm: str  
    driver_address: str
    driver_lat: float = 0.0
    driver_long: float = 0.0


class update_location_model(BaseModel):
    driver_lan: float
    driver_long: float