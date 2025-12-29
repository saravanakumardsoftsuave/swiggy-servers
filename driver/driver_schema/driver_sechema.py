from sqlalchemy import Column,Float,Integer,String,Boolean,DateTime,ForeignKey,BigInteger
from sqlalchemy.orm import relationship
from  database import base
from datetime import datetime, timezone

class driver_details(base):
    __tablename__ = 'driver_details'

    id = Column(Integer, primary_key=True, index=True)
    driver_name = Column(String, nullable=False)
    driver_bike_no = Column(String, nullable=False)
    driver_license_no = Column(String, nullable=False)
    driver_phone_no = Column(BigInteger, nullable=False)
    driver_email = Column(String, nullable=False, unique=True)
    driver_password = Column(String, nullable=False)
    driver_address = Column(String, nullable=False)
    driver_lat = Column(Float, nullable=False)
    driver_long = Column(Float, nullable=False)
    driver_rating = Column(Float, default=0.0)
    driver_status = Column(Boolean, default=False)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )