from fastapi import FastAPI
from driver_route.driver_route import driver_route

from database import engine, base
from driver_schema import driver_sechema

app = FastAPI(title="Driver Service")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)

app.include_router(driver_route)
