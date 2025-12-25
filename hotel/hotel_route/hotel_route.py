from fastapi import APIRouter,Depends,HTTPException,status
from hotel_models.hotel_models import drive_model,update_location_model
from database import get_db
from hotel_service.hotel_service import driver_service
from fastapi.security import OAuth2PasswordRequestForm
from hotel_service.hotel_service import token,get_user
hotel_route=APIRouter(prefix='/driver',tags=['Driver'])


@hotel_route.post('/signup')
async def driver_singup(driver: drive_model, db=Depends(get_db)):
    service = driver_service(db)
    await service.create_driver(driver)
    return {"message":"Driver created successfully"}
@hotel_route.post('/login')
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

@hotel_route.get('/current_driver')
async def current_driver(user=Depends(get_user)):
     return {"driver_name": user.driver_name}
    
@hotel_route.put('/update_location')
async def update_location_(email:str,location: update_location_model, db=Depends(get_db)):
    location_data = driver_service(db)
    await location_data.update_location_(email, location)
    return {"message": "Location updated successfully"}

@hotel_route.get('/request_ride')
async def request_ride():
    pass


@hotel_route.put('/update_status')
async def update_status():
    pass
