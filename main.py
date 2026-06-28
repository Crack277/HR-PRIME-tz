from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.database.database_helper import db_helper
from src.router import router as router_v1
from src.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await db_helper.engine.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(router_v1)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
