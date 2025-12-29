from user_utils.user_utils import hash_password,verify_password
from sqlalchemy.future import select
from fastapi import HTTPException, status
from user_models.users_model import user_model,order_model,food_items,update_location_model,payment_status
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
    
    async def order_create(self,order:order_model):
        result = await self.db.execute(
    text("SELECT 1 FROM hotel_details WHERE id = :hid"),
    {"hid": order.hotel_id})
        if result.scalar() is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='invalid')
        user=await self.db.scalar(select(user_details).where(user_details.user_id==order.user_id))
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='invalid user_id')
        new_oder=orders(
            user_id=order.user_id,
            hotel_id=order.hotel_id,
            total_amount=0,
        )
        self.db.add(new_oder)
        await self.db.flush()
        total_amount=0
    
        for items in order.items:
            food = await self.db.scalar(text("SELECT item_price FROM food_item_details WHERE id =:hid"),
                                         {'hid':items.food_id})
            if food is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid food id')
            card=order_items(
                order_id=new_oder.id,
                food_id=items.food_id,
                quantity=items.quantity
            )
            self.db.add(card)
        
            total_amount+=food*items.quantity

        new_oder.total_amount=total_amount
        await self.db.execute(text('UPDATE orders SET order_status = :status where id= :oid'),
                                  {'status':'Waiting For order confirmation',
                                   'oid':new_oder.id})
            
        await self.db.commit()
        await self.db.refresh(new_oder)
            
        return {
    "order_id": new_oder.id,
    "user_id": new_oder.user_id,
    "hotel_id": new_oder.hotel_id,
    "total_amount": new_oder.total_amount,
    "items": order.items   }
     
    async def payment_status_(self,order_id:int,payment:payment_status):
        order_status_=await self.db.scalar(select(orders).where(orders.order_status=='order Conformed'))
        if order_status_:
            order=await self.db.scalar(select(orders).where(orders.id==order_id))
            if order is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid order_id')
            if payment.payment_method=='Online':
                await self.db.execute(text('UPDATE orders SET payment_status =:status WHERE id =:oid'),
                                    {
                                        'status':'PAID',
                                        'oid':order_id
                                    })
                self.db.commit()
            elif payment.payment_method=='Cash_On_Delivery':
                await self.db.execute(text('UPDATE orders SET payment_status =:status WHERE id =:oid'),
                                    {
                                        'status':'NOT PAID,CASH_ON_DELIVERY',
                                        'oid':order_id
                                    })
                self.db.commit()
            return {
                'message':'status updated'
            }
        elif not order_status_:
            return {
                'message':'Your order still in order conformation'
            }
            