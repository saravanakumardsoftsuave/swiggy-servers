from fastapi import FastAPI
from hotel_route.hotel_route import hotel_route
from database import base,engine
from hotel_schema import hotel_schema
app=FastAPI()

app.include_router(hotel_route)

@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)