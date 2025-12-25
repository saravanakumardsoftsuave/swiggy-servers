
from pydantic import BaseModel

class drive_model(BaseModel):
    driver_name: str
    drive_bike_no: str
    drive_license_no: str
    drive_phone_no: int
    driver_email: str
    driver_password: str
    driver_password_confirm: str  
    drive_address: str
    driver_lan: float = 0.0
    driver_long: float = 0.0


class update_location_model(BaseModel):
    driver_lan: float
    driver_long: float