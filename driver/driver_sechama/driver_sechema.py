# driver_sechema.py (schema table)
from sqlalchemy import BigInteger, Column, Float, Integer, String, Boolean, DateTime
from database import base
from datetime import datetime, timezone

class driver_details(base):
    __tablename__ = 'driver_details'
    id = Column(Integer, primary_key=True, index=True)
    driver_name = Column(String, nullable=False)
    drive_bike_no = Column(String, nullable=False)
    drive_license_no = Column(String, nullable=False)
    drive_phone_no = Column(BigInteger, nullable=False) 
    driver_email = Column(String, nullable=False, unique=True)
    drive_password = Column(String, nullable=False)
    drive_address = Column(String, nullable=False)
    driver_lan = Column(Float, nullable=False)
    driver_long = Column(Float, nullable=False)
    driver_rating = Column(Float, default=0.0)  
    driver_status = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)