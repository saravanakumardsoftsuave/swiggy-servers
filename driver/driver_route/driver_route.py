from fastapi import APIRouter,Depends,HTTPException,status
from driver_models.driver_model import drive_model,update_location_model,orderrequest,update_status
from database import get_db
from driver_service.driver_service import driver_service
from fastapi.security import OAuth2PasswordRequestForm
from driver_utils.driver_utils import token,get_user
driver_route=APIRouter(prefix='/driver',tags=['Driver'])


@driver_route.post('/signup',status_code=status.HTTP_201_CREATED)
async def driver_singup(driver: drive_model, db=Depends(get_db)):
    service = driver_service(db)
    driver_new=await service.create_driver(driver)
    return {
         'driver_id':driver_new.id,
         "message":"Driver created successfully"}
@driver_route.post('/login')
async def driver_login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db=Depends(get_db)
):

        service = driver_service(db)
        user = await service.driver_login(form_data.username, form_data.password)
        ref=await token(data={"sub": user.driver_name})
        return {
             'access_token': ref,
            'token_type': 'bearer',
            "message": "Login successful",
            "driver_id": user.id,
            "driver_name": user.driver_name
        }

@driver_route.get('/current_driver')
async def current_driver(user=Depends(get_user)):
     return {"driver_name": user.driver_name}
    
@driver_route.put('/update_location')
async def update_location_(location: update_location_model, db=Depends(get_db),user=Depends(get_user)):
    location_data = driver_service(db)
    await location_data.update_location_(user, location)
    return {"message": "Location updated successfully"}

@driver_route.post('/request_ride')
async def request_ride(order:orderrequest,db=Depends(get_db),user=Depends(get_user)):
    result=driver_service(db)
    return await result.Orderrequest(order,user)



@driver_route.put('/update_status')
async def update_status(status_driver:update_status,db=Depends(get_db),user=Depends(get_user)):
     result=driver_service(db)
     return await result.update_status(status_driver,user)


@driver_route.delete('/delete_driver')

async def delete_driver(db=Depends(get_db),user=Depends(get_user)):
     result=driver_service(db)
     return await result.delete_user(user)