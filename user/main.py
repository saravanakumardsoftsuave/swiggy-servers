
from contextlib import asynccontextmanager
from fastapi import FastAPI

from user_route.user_route import user_route
from database import engine, base
from user_schema import user_schema

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

app.include_router(user_route)
