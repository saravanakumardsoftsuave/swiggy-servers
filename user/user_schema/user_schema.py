from sqlalchemy import Column,Float,Integer,String,Boolean,DateTime,ForeignKey,BigInteger
from sqlalchemy.orm import relationship
from database import base
from datetime import datetime, timezone

class user_details(base):
    __tablename__ = 'user_details'

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    user_phone_no = Column(BigInteger, nullable=False)
    user_email = Column(String, nullable=False, unique=True)
    user_password = Column(String, nullable=False)
    user_address = Column(String, nullable=False)
    user_lat = Column(Float, nullable=False)
    user_long = Column(Float, nullable=False)

    orders = relationship("orders", back_populates="user")

class orders(base):
    __tablename__ = 'orders'
    id=Column(Integer,primary_key=True,index=True)
    ordeitem_id = Column(Integer, ForeignKey('order_items.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user_details.user_id'), nullable=False)
    hotel_id = Column(Integer,  nullable=False)
    order_status = Column(String, default="INITIAL")
    total_amount = Column(Float, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user = relationship("user_details", back_populates="orders")
    order_items = relationship("order_items",back_populates="order")

class order_items(base):
    __tablename__ = 'order_items'
    id=Column(Integer,primary_key=True,index=True)
    order_id = Column(Integer, nullable=True)
    food_id = Column(Integer, ForeignKey('food_item_details.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("orders", back_populates="order_items")