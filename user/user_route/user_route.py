from fastapi import APIRouter,Depends,HTTPException,status
from user_models.users_model import user_model,order_model,food_items,update_location_model,payment_status
from database import get_db
from user_schema.user_schema import user_details,order_items,orders
from user_service.user_service import Userservice
from fastapi.security import OAuth2PasswordRequestForm
from user_utils.user_utils import token,get_user
user_route=APIRouter(prefix='/user',tags=['USER'])


@user_route.post('/signup',status_code=status.HTTP_201_CREATED)
async def user_singup(user:user_model, db=Depends(get_db)):
    service = Userservice(db)
    new_user=await service.user_create(user)
    return {
         'user_id':new_user.user_id,
         "message":"user created successfully"}

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

@user_route.get('/currentUser')
async def current_user(user=Depends(get_user)):
     return {"user_name": user.user_name}
    
@user_route.put('/update_location')
async def update_location_(location: update_location_model, db=Depends(get_db),auth=Depends(get_user)):
    location_data = Userservice(db)
    await location_data.update_location_( location,auth)
    return {"message": "Location updated successfully"}

@user_route.post('/ordering')
async def orders_(order:order_model,db=Depends(get_db),auth=Depends((get_user))):
     orders=Userservice(db)
     orderr=await orders.order_create(order,auth)
     return orderr

@user_route.put('/update_order_status')
async def update_payment_status(order_id:int,payment:payment_status,db=Depends(get_db),auth=Depends((get_user))):
    result=Userservice(db)
    return await result.payment_status_(order_id,payment,auth)

async def delete_driver(db=Depends(get_db),user=Depends(get_user)):
     result=Userservice(db)
     return await result.delete_user(user)
