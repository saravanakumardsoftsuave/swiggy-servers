from fastapi import APIRouter,Depends,HTTPException,status
from user_models.users_model import user_model,order_model,food_items,update_location_model,payment_status
from database import get_db
from user_schema.user_schema import user_details,order_items,orders
from user_service.user_service import Userservice
from fastapi.security import OAuth2PasswordRequestForm
from user_utils.user_utils import token,get_user
user_route=APIRouter(prefix='/user',tags=['USER'])


@user_route.post('/signup')
async def user_singup(hotel:user_model, db=Depends(get_db)):
    service = Userservice(db)
    await service.user_create(hotel)
    return {"message":"user created successfully"}

@user_route.post('/login')
async def  user_login_(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db=Depends(get_db)
):
        service = Userservice(db)
        user = await service.user_login(form_data.username, form_data.password)
        ref=await token(data={"sub": user.user_name})
        return {
             'access_token': ref,
            'token_type': 'bearer',
            "message": "Login successful",
            "driver_id": user.user_id,
            "driver_name": user.user_name
        }

@user_route.get('/current_hotel')
async def current_hotel(user=Depends(get_user)):
     return {"user_name": user.user_name}
    
@user_route.put('/update_location')
async def update_location_(email:str,location: update_location_model, db=Depends(get_db)):
    location_data = Userservice(db)
    await location_data.update_location_(email, location)
    return {"message": "Location updated successfully"}

@user_route.post('/ordering')
async def orders_(order:order_model,db=Depends(get_db)):
     orders=Userservice(db)
     orderr=await orders.order_create(order)
     return orderr

@user_route.put('/update_status')
async def update_payment_status(order_id:int,payment:payment_status,db=Depends(get_db),auth=Depends((get_user))):
    result=Userservice(db)
    return await result.payment_status_(order_id,payment)
