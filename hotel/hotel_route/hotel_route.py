from fastapi import APIRouter,Depends,HTTPException,status
from hotel_models.hotel_models import hotel_model,update_location_model,category_model,food_item_model,Orderrequest
from database import get_db
from hotel_service.hotel_service import Hotelservice
from fastapi.security import OAuth2PasswordRequestForm
from hotel_utils.hotel_utils import token,get_user
hotel_route=APIRouter(prefix='/hotel',tags=['HOTEL'])


@hotel_route.post('/signup',status_code=status.HTTP_201_CREATED)
async def hotel_singup(hotel:hotel_model, db=Depends(get_db)):
    service = Hotelservice(db)
    hotel_new=await service.create_hotel(hotel)
    return {
         'hotel_id':hotel_new.id,
         "message":"Hotel created successfully"}

@hotel_route.post('/login')
async def  hotel_login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db=Depends(get_db)
):
        service = Hotelservice(db)
        user = await service.hotel_login(form_data.username, form_data.password)
        ref=await token(data={"sub": user.hotel_name})
        return {
             'access_token': ref,
            'token_type': 'bearer',
            "message": "Login successful",
            "hotel_id": user.id,
            "hotel_name": user.hotel_name
        }

@hotel_route.get('/current_hotel')
async def current_hotel(user=Depends(get_user)):
     return {"hotel_name": user.hotel_name}
    
@hotel_route.put('/update_location')
async def update_location_(location: update_location_model, db=Depends(get_db),user=Depends(get_user)):
    location_data = Hotelservice(db)
    await location_data.update_location_(location,user)
    return {"message": "Location updated successfully"}

@hotel_route.post('/category')
async def  create_category(data:category_model,db=Depends(get_db),user=Depends(get_user)):
    category=Hotelservice(db)
    category_=await category.create_cat(data,user)
    return {
         'message':'category created',
         'category_name':category_.category_name
    }

@hotel_route.post('/food_item')
async def food_items(data:food_item_model,db=Depends(get_db),user=Depends(get_user)):
     food_item=Hotelservice(db)
     food_item_=await food_item.create_foods(data,user)
     return{
          'message':'food created',
          'food_name':food_item_.item_name
     }


@hotel_route.post('/orderrequest')
async def orderrequest(order:Orderrequest,db=Depends(get_db),user=Depends(get_user)):
    result=Hotelservice(db)
    return await result.orders(order,user)

async def delete_driver(db=Depends(get_db),user=Depends(get_user)):
     result=Hotelservice(db)
     return await result.delete_user(user)