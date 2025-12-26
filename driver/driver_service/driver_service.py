from driver_utils.driver_utils import hash_password,verify_password
from sqlalchemy.future import select
from fastapi import HTTPException, status
from driver_models.driver_model import drive_model,update_location_model
from driver_schema.driver_sechema import driver_details

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
            select(driver_details).where(driver_details.driver_email == email)
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