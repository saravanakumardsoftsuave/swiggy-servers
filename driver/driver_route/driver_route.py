from fastapi import APIRouter,Depends,HTTPException,status
from driver_models.driver_model import drive_model,update_location_model,orderrequest,update_status
from database import get_db
from driver_service.driver_service import driver_service
from fastapi.security import OAuth2PasswordRequestForm
from driver_utils.driver_utils import token,get_user
driver_route=APIRouter(prefix='/driver',tags=['Driver'])


@driver_route.post('/signup')
async def driver_singup(driver: drive_model, db=Depends(get_db)):
    service = driver_service(db)
    await service.create_driver(driver)
    return {"message":"Driver created successfully"}
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
async def update_location_(email:str,location: update_location_model, db=Depends(get_db)):
    location_data = driver_service(db)
    await location_data.update_location_(email, location)
    return {"message": "Location updated successfully"}

@driver_route.post('/request_ride')
async def request_ride(driver_id:int,order:orderrequest,db=Depends(get_db)):
    result=driver_service(db)
    return await result.Orderrequest(driver_id,order)



@driver_route.put('/update_status')
async def update_status(status_driver:update_status,db=Depends(get_db)):
     result=driver_service(db)
     return await result.update_status(status_driver)
