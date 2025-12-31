from sqlalchemy import Column,Float,Integer,String,Boolean,DateTime,ForeignKey,BigInteger
from sqlalchemy.orm import relationship
from database import base
from datetime import datetime, timezone

class hotel_details(base):
    __tablename__ = 'hotel_details'

    id = Column(Integer, primary_key=True, index=True)
    hotel_name = Column(String, nullable=False)
    hotel_phone_no = Column(BigInteger, nullable=False)
    hotel_email = Column(String, nullable=False, unique=True)
    hotel_password = Column(String, nullable=False)
    hotel_address = Column(String, nullable=False)
    hotel_lat = Column(Float, nullable=False)
    hotel_long = Column(Float, nullable=False)
    hotel_rating = Column(Float, default=0.0)
    hotel_status = Column(Boolean, default=False)
    hotel_delete=Column(Boolean,default=False,nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    categories = relationship("category_details", back_populates="hotel")
    food_items = relationship("food_item_details", back_populates="hotel")

class category_details(base):
    __tablename__ = 'category_details'

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey('hotel_details.id'), nullable=False)
    category_name = Column(String, nullable=False)
    category_description = Column(String, nullable=True)

    hotel = relationship("hotel_details", back_populates="categories")
    food_items = relationship("food_item_details", back_populates="category")

class food_item_details(base):
    __tablename__ = 'food_item_details'

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, nullable=False)
    item_description = Column(String, nullable=True)
    item_price = Column(Float, nullable=False)
    hotel_id = Column(Integer, ForeignKey('hotel_details.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('category_details.id'), nullable=False)
    
    category = relationship("category_details", back_populates="food_items")
    hotel = relationship("hotel_details", back_populates="food_items")