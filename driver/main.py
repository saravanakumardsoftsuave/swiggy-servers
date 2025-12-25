from fastapi import FastAPI
from driver_route.driver_route import driver_route

app=FastAPI()

app.include_router(driver_route)