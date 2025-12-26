from fastapi import FastAPI
from user_route.user_route import user_route
from database import base,engine
from user_schema import user_schema
app=FastAPI()

app.include_router(user_route)

@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)