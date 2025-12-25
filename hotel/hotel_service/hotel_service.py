from hotel_utils.hotel_utils import hash_password,verify_password
from sqlalchemy.future import select
from fastapi import HTTPException, status
from hotel_models.hotel_models import drive_model,update_location_model
from hotel_sechema.hotel_sechema import driver_details

class driver_service:
    def __init__(self, db):
        self.db = db
    
    async def create_driver(self, driver: drive_model) -> driver_details:
        result = await self.db.execute(
            select(driver_details).where(
                driver_details.driver_email == driver.driver_email
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
            drive_bike_no=driver.drive_bike_no,
            drive_license_no=driver.drive_license_no,
            drive_phone_no=driver.drive_phone_no,
            driver_email=driver.driver_email,
            drive_password=driver_password,  
            drive_address=driver.drive_address,
            driver_lan=driver.driver_lan,
            driver_long=driver.driver_long,
            driver_rating=0.0
        )
        self.db.add(new_driver)
        await self.db.commit()
        await self.db.refresh(new_driver)
        return new_driver

    async def driver_login(self, email: str, password: str) -> driver_details:
        result = await self.db.execute(
            select(driver_details).where(driver_details.driver_email == email)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        is_valid = verify_password(password, user.drive_password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        return user
    async def update_location_(self, email: str, location:update_location_model):
        user= await self.db.execute(select(driver_details).where(driver_details.driver_email==email))
        driver=user.scalar_one_or_none()
        if not driver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found"
            )
        driver.driver_lan=location.driver_lan
        driver.driver_long=location.driver_long
        driver.driver_status=True
        await self.db.commit()
        await self.db.refresh(driver)
        return driver