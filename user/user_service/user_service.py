from user_utils.user_utils import hash_password,verify_password
from sqlalchemy.future import select
from fastapi import HTTPException, status
from user_models.users_model import user_model,order_model,food_items,update_location_model
from user_schema.user_schema import user_details,order_items,orders
from sqlalchemy import text
class  Userservice:
    def __init__(self, db):
        self.db = db
    async def user_create(self, user: user_model) -> user_model:
        user_ = await self.db.scalar(
            select(user_details).where(
                user_details.user_email == user.user_email
            )
        )
        if user_:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user with this email already exists"
            )
        if user.user_password != user.user_password_confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password and Confirm Password do not match"
            )
        user_password = hash_password(user.user_password)
        new_user = user_details(
            user_name=user.user_name,
            user_phone_no=user.user_phone_no,
            user_email=user.user_email,
            user_password=user_password,  
            user_address=user.user_address,
            user_lat=user.user_lat,
            user_long=user.user_long,
           
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def user_login(self, email: str, password: str) -> user_details:
        user = await self.db.scalar(
            select(user_details).where(user_details.user_email == email)
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        is_valid = verify_password(password, user.user_password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        return user
    async def update_location_(self, email: str, location:update_location_model):
        user= await self.db.scalar(select(user_details).where(user_details.user_email==email))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found"
            )
        user.user_lat=location.user_lat
        user.user_long=location.user_long
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def orderitem(self,order:food_items):
        result=await self.db.execute(text("SELECT 1 FROM food_item_details WHERE id=:hid"),{'hid':order.food_id})
        if result.scalar() is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid food id')
        new_orderitem=order_items(
            order_id=order.order_id,
            food_id=order.food_id,
            quantity=order.quantity
        )
        self.db.add(new_orderitem)
        self.db.commit()
        self.db.refresh(new_orderitem)
        return new_orderitem
    async def order_create(self,order:order_model):
        result = await self.db.execute(
    text("SELECT 1 FROM hotel_details WHERE id = :hid"),
    {"hid": order.hotel_id}
)
        if result.scalar() is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='invalid')
        user=await self.db.scalar(select(user_details).where(user_details.user_id==order.user_id))
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='invalid user_id')
        new_oder=orders(
            user_id=order.user_id,
            hotel_id=order.hotel_id,
            driver_id=order.driver_id,
            total_amount=order.total_amount,
        )

        self.db.add(new_oder)
        await self.db.commit()
        await self.db.refresh(new_oder)
        return new_oder       
    # async def orderitem(self,order:orderItem):
    #     result=await self.db.execute(text("SELECT 1 FROM "))

    # async def create_cat(self,data:category_model):
    #     check_hotel_id=await self.db.scalar(select(hotel_details).where(hotel_details.id==data.hotel_id))
    #     if not check_hotel_id:
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid hotel_id')
    #     category=await self.db.scalar(select(category_details).where(category_details.category_name==data.category_name))
    #     if category:
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='The Category name was already in ')
    #     category_new=category_details(
    #         hotel_id=data.hotel_id,
    #         category_name=data.category_name,
    #         category_description=data.category_description
    #     )

    #     self.db.add(category_new)
    #     await self.db.commit()
    #     await self.db.refresh(category_new)

    #     return category_new
    
    # async def create_foods(self,data:dict):
    #     check_category_id=await self.db.scalar(select(category_details).where(category_details.id==data.category_id))
    #     if not check_category_id:
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid category_id')
    #     food=await self.db.scalar(select(food_item_details).where(food_item_details.item_name==data.item_name,
    #                                                               food_item_details.category_id==data.category_id))
    #     if  food:
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='The food_name already in')
        
    #     new_food_item=food_item_details(
    #         category_id=data.category_id,
    #          hotel_id=check_category_id.hotel_id,
    #          item_name=data.item_name,
    #          item_description=data.item_description,
    #          item_price=data.item_price

    #     )
    #     self.db.add(new_food_item)
    #     await self.db.commit()
    #     await self.db.refresh(new_food_item)
    #     return new_food_item