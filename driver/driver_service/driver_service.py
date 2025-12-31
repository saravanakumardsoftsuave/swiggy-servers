from driver_utils.driver_utils import hash_password,verify_password,get_user
from fastapi import Depends
from sqlalchemy.future import select
from fastapi import HTTPException, status
from driver_models.driver_model import drive_model,update_location_model,orderrequest
from driver_schema.driver_sechema import driver_details
from sqlalchemy import text
class driver_service:
    def __init__(self, db):
        self.db = db
    
    async def create_driver(self, driver: drive_model) -> driver_details:
        result = await self.db.execute(
            select(driver_details).where(
                driver_details.driver_email == driver.driver_email,driver_details.driver_delete==False
            )
        )
        user = result.scalar_one_or_none()
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Driver with this email already exists"
            )
        if driver.driver_password != driver.driver_password_confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password and Confirm Password do not match"
            )
        driver_password = hash_password(driver.driver_password)
        new_driver = driver_details(
            driver_name=driver.driver_name,
            driver_bike_no=driver.driver_bike_no,
            driver_license_no=driver.driver_license_no,
            driver_phone_no=driver.driver_phone_no,
            driver_email=driver.driver_email,
            driver_password=driver_password,  
            driver_address=driver.driver_address,
            driver_lat=driver.driver_lat,
            driver_long=driver.driver_long,
            driver_rating=0.0
        )
        self.db.add(new_driver)
        await self.db.commit()
        await self.db.refresh(new_driver)
        return new_driver

    async def driver_login(self, email: str, password: str) -> driver_details:
        result = await self.db.execute(
            select(driver_details).where(driver_details.driver_email == email,driver_details.driver_delete == False)
        )
        user = result.scalar_one_or_none()
       

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        is_valid = verify_password(password, user.driver_password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        return user
    async def update_location_(self, user, location:update_location_model):
        driver_user= await self.db.execute(select(driver_details).where(driver_details.driver_name==user.driver_name,driver_details.driver_delete == False))
        driver=driver_user.scalar_one_or_none()
        if not driver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found"
            )
        driver.driver_lat=location.driver_lat
        driver.driver_long=location.driver_long
        driver.driver_status=True
        await self.db.commit()
        await self.db.refresh(driver)
        return driver
    
    async def Orderrequest(self,order:orderrequest,user=Depends(get_user)):
        driver_user= await self.db.execute(select(driver_details).where(driver_details.driver_name==user.driver_name,driver_details.driver_delete == False))
        driver=driver_user.scalar_one_or_none()
        if not driver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found"
            )
        order_status_=await self.db.scalar(text('SELECT order_status from orders where id= :oid'),
                                        {'oid':order.order_id})
        if order_status_!='Waiting For order confirmation':
                access=await self.db.scalar(text('SELECT driver_name FROM orders WHERE id  =:oid'),
                                                {
                                                    'oid':order.order_id
                                                })
                if access == 'None':
                    driver_name=await self.db.scalar(
                    select(driver_details).where(driver_details.driver_name == user.driver_name)
                )
                    if driver_name is None:
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid driver_id')
                
                    await self.db.execute(text('UPDATE orders SET driver_name  =:name where id =:oid'),
                                            {'name':driver_name.driver_name,
                                            'oid':order.order_id})
                    if order.response=='Accept':
                        hotelid=await self.db.execute(text('SELECT hotel_name,hotel_phone_no,hotel_lat,hotel_long FROM hotel_details WHERE id= :hid'),
                                                        {'hid':order.hotel_id})
                        order_=await self.db.execute(text('SELECT food_id, quantity FROM order_items WHERE id= :oid'),
                                                    {
                                                        'oid':order.order_id
                                                    })
                        userid=await self.db.execute(text('SELECT user_name,user_phone_no,user_lat,user_long FROM user_details WHERE user_id= :uid'),
                                                        {'uid':order.user_id}) 
                        
                        total_amt=await self.db.scalar(text('SELECT total_amount FROM orders WHERE id= :uid'),
                                                        {'uid':order.order_id})
                        if hotelid is None:
                            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid Hotel_id')
                        if userid is None:
                            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid user_id')
                        

                        orders=order_.all()
                        items=[]
                        for item in orders:
                            food_name=await self.db.scalar(text('SELECT item_name FROM food_item_details WHERE id = :fid'),{'fid':item.food_id})
                            items.append({
                                'food_name':food_name,
                                'quantity':item.quantity
                            })

                        hotel_locations=hotelid.all()
                        hotel_location=[]
                        for loc in hotel_locations:
                            hotel_location.append({
                                'hotel_name':loc.hotel_name,
                                'hotel_phone_no':loc.hotel_phone_no,
                                'hotel_lat':loc.hotel_lat,
                                'hotel_long':loc.hotel_long
                            })

                    
                        row = userid.fetchone()
                        if row is None:
                            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid user_id')

                        user_location = [{
                            'user_name': row.user_name,
                            'user_phone_no': row.user_phone_no,
                            'user_lat': row.user_lat,
                            'user_long': row.user_long
                        }]

                        status=await self.db.execute(text('UPDATE orders SET order_status = :status where id= :oid'),
                                            {'status':'DRIVER ASSIGNED',
                                            'oid':order.order_id})
                        
                        return {
                                    'order_id':order.order_id,
                                    'hotel_details':hotel_location,
                                    'user_details':user_location,
                                    'orderitems':items,
                                    'total_amount':total_amt
                                }
                    else:
                        return {'message':'Your order point will lose'}
                else:
                    return {'message':'Order already took'}
        else:
            return {'message': 'Waiting For order confirmation' }
    async def update_status(self,status_driver:update_status,user=Depends(get_user)):
        driver_user= await self.db.execute(select(driver_details).where(driver_details.driver_name==user.driver_name,driver_details.driver_delete == False))
        driver=driver_user.scalar_one_or_none()
        if not driver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found"
            )
        
        ord_status=await self.db.scalar(text('SELECT order_status FROM orders WHERE id  =:oid'),
                                            {
                                                'oid':status_driver.order_id
                                            })
        if (ord_status=='ORDER DELIVERIED' and status_driver.current_status!='ORDER DELIVERIED') or ord_status=='ORDER DELIVERIED':
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail='THE ORDER AREADY COMPLETED?')
        if ord_status=='ON THE WAY' and status_driver.current_status=='ORDER PICKED' or ord_status=='ON THE WAY':
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail='THE ORDER AREADY ON THE WAY?')
        if ord_status=='ORDER PICKED' and status_driver.current_status=='ORDER PICKED':
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail='THE ORDER AREADY PICKED?')
        access=await self.db.scalar(text('SELECT driver_name FROM orders WHERE id  =:oid'),
                                                {
                                                    'oid':status_driver.order_id
                                                })
        if access == 'None':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Driver Not Assigned')
        status_=await  self.db.execute(text('UPDATE orders SET order_status= :status WHERE id= :oid'),
                                    {'status':status_driver.current_status,
                                    'oid':status_driver.order_id})
        if status_ is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invald order_id')
        # order_status=await self.db.scalar(text('SELECT order_status FROM orders WHERE id  =:oid'),
        #                                     {
        #                                         'oid':status_driver.order_id
        #                                     })
        # if 
        payment_status=await self.db.scalar(text('SELECT payment_status FROM orders WHERE id  =:oid'),
                                            {
                                                'oid':status_driver.order_id
                                            })
        if payment_status=='NOT PAID,CASH_ON_DELIVERY' and status_driver.current_status=='ORDER DELIVERIED':
            await  self.db.execute(text('UPDATE orders SET payment_status= :status WHERE id= :oid'),
                                    {'status':'PAID',
                                    'oid':status_driver.order_id})
            return {
            'message':'AMOUNT PAID AND ORDER DELIVERIED!!!'
        }
        elif payment_status=='PAID' and status_driver.current_status=='ORDER DELIVERIED':
            return{'message':'order completed!!!'}
        return {
            'message':'Your order status Updated!!!'
        }
    async def delete_user(self,user=Depends(get_user)):
        delt= await self.db.scalar(select(driver_details).where(driver_details.driver_name==user.driver_name,driver_details.driver_delete == False))
        if not delt:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid user')
        delt.driver_delete=True
        await self.db.commit()
        return {
            "driver_id":delt.id,
            'message':'driver account deleted'
        }

