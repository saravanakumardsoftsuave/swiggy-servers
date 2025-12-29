
from contextlib import asynccontextmanager
from fastapi import FastAPI

from hotel_route.hotel_route import hotel_route
from database import engine, base
from hotel_schema import hotel_schema

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)

    yield 

    await engine.dispose()

app = FastAPI(
    title="Hotel Service",
    lifespan=lifespan
)

app.include_router(hotel_route)
