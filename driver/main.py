from contextlib import asynccontextmanager
from fastapi import FastAPI

from driver_route.driver_route import driver_route
from database import engine, base
from driver_schema import driver_sechema  

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)

    yield 

    await engine.dispose()

app = FastAPI(
    title="Driver Service",
    lifespan=lifespan
)

app.include_router(driver_route)
