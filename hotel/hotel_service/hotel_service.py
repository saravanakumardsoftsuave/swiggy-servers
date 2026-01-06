from hotel_utils.hotel_utils import hash_password,verify_password,get_user
from sqlalchemy.future import select
from fastapi import HTTPException, status,Depends
from hotel_models.hotel_models import hotel_model,update_location_model,category_model,food_item_model,Orderrequest,update_pass
from hotel_schema.hotel_schema import hotel_details,category_details,food_item_details
from sqlalchemy import text
class Hotelservice:
    def __init__(self, db):
        self.db = db
    
    async def create_hotel(self, hotel: hotel_model) -> hotel_details:
        result = await self.db.execute(
            select(hotel_details).where(
                hotel_details.hotel_email == hotel.hotel_email
            )
        )
        user = result.scalar_one_or_none()
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Hotel with this email already exists"
            )
        if hotel.hotel_password != hotel.hotel_password_confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password and Confirm Password do not match"
            )
        hotel_password = hash_password(hotel.hotel_password)
        new_hotel = hotel_details(
            hotel_name=hotel.hotel_name,
            hotel_phone_no=hotel.hotel_phone_no,
            hotel_email=hotel.hotel_email,
            hotel_password=hotel_password,  
            hotel_address=hotel.hotel_address,
            hotel_lat=hotel.hotel_lat,
            hotel_long=hotel.hotel_long,
            hotel_rating=0.0
        )
        self.db.add(new_hotel)
        await self.db.commit()
        await self.db.refresh(new_hotel)
        return new_hotel

    async def hotel_login(self, email: str, password: str) -> hotel_details:
        result = await self.db.execute(
            select(hotel_details).where(hotel_details.hotel_email == email,hotel_details.hotel_delete == False)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        is_valid = verify_password(password, user.hotel_password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        return user
    async def update_location_(self, location:update_location_model,user=Depends(get_user)):
        use_r= await self.db.execute(select(hotel_details).where(hotel_details.hotel_name==user.hotel_name,hotel_details.hotel_delete == False))
        hotel=use_r.scalar_one_or_none()
        if not hotel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found"
            )
        hotel.hotel_lat=location.hotel_lat
        hotel.hotel_long=location.hotel_long
        hotel.hotel_status=True
        await self.db.commit()
        await self.db.refresh(hotel)
        return hotel
    

    async def create_cat(self,data:category_model,user=Depends(get_user)):
        use_r= await self.db.execute(select(hotel_details).where(hotel_details.hotel_name==user.hotel_name,hotel_details.hotel_delete == False))
        hotel=use_r.scalar_one_or_none()
        if not hotel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found"
            )
        check_hotel_id=await self.db.scalar(select(hotel_details).where(hotel_details.id==data.hotel_id))
        if not check_hotel_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid hotel_id')
        category=await self.db.scalar(select(category_details).where(category_details.category_name==data.category_name,category_details.hotel_id == data.hotel_id))
        if category and check_hotel_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='The Category name was already in ')
        category_new=category_details(
            hotel_id=data.hotel_id,
            category_name=data.category_name,
            category_description=data.category_description
        )

        self.db.add(category_new)
        await self.db.commit()
        await self.db.refresh(category_new)

        return category_new
    
    async def create_foods(self,data:dict,user=Depends(get_user)):
        use_r= await self.db.execute(select(hotel_details).where(hotel_details.hotel_name==user.hotel_name,hotel_details.hotel_delete == False))
        hotel=use_r.scalar_one_or_none()
        if not hotel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found"
            )
        check_category_id=await self.db.scalar(select(category_details).where(category_details.id==data.category_id))
        if not check_category_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid category_id')
        food=await self.db.scalar(select(food_item_details).where(food_item_details.item_name==data.item_name,
                                                                  food_item_details.category_id==data.category_id))
        if  food:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='The food_name already in')
        
        new_food_item=food_item_details(
            category_id=data.category_id,
             hotel_id=check_category_id.hotel_id,
             item_name=data.item_name,
             item_description=data.item_description,
             item_price=data.item_price

        )
        self.db.add(new_food_item)
        await self.db.commit()
        await self.db.refresh(new_food_item)
        return new_food_item
    async def orders(self,order:Orderrequest,user=Depends(get_user)):
        use_r= await self.db.execute(select(hotel_details).where(hotel_details.hotel_name==user.hotel_name,hotel_details.hotel_delete == False))
        hotel=use_r.scalar_one_or_none()
        if not hotel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found"
            )
        if  order.response=='accept':
            orders=await self.db.scalar(text('SELECT total_amount from orders where id= :oid'),
                                        {'oid':order.order_id})
            if orders is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid order id')
            orderitems=await self.db.execute(text("SELECT food_id,quantity FROM order_items WHERE order_id= :oid"),
                                           {'oid':order.order_id})
            await self.db.execute(text('UPDATE orders SET order_status = :status where id= :oid'),
                                  {'status':'order Conformed',
                                   'oid':order.order_id})
            
            orderitem=orderitems.all()
            item=[]
            for itm in orderitem:
                food_name=await self.db.scalar(text('SELECT item_name from food_item_details WHERE id= :fid'),
                                               {'fid':itm.food_id})
                if food_name:
                    item.append({
                    'food_name':food_name,
                    'food_id':itm.food_id,
                    'quantity':itm.quantity
                })

            if orderitem is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid orderitem')
            return{
                'order_id':order.order_id,
                'orderitems':item,
                'total_amount':orders
            }
        else:
            return {'message':'order cancelled'}
    async def delete_user(self,user=Depends(get_user)):
        delt= await self.db.scalar(select(hotel_details).where(hotel_details.hotel_name==user.hotel_name,hotel_details.hotel_delete == False))
        if not delt:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid user')
        delt.hotel_delete=True
        self.db.commit()
        return {
            "hotel_id":delt.id,
            'message':'driver account deleted'
        }
    
    async def updatePass(self,updatepass:update_pass):
        use_r= await self.db.execute(select(hotel_details).where(hotel_details.id==updatepass.hotel_id,hotel_details.hotel_delete == False))
        hotel=use_r.scalar_one_or_none()
        if not hotel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,detail='user not found')
        passw=hash_password(updatepass.password)

        hotel.hotel_password=passw
        await self.db.commit()
        return {'message':'password updated'}
