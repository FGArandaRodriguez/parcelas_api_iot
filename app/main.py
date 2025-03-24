import asyncio

from fastapi import FastAPI
from app.api.socket import router as socket_router, poll_and_broadcast
from app.core.database import get_db


app = FastAPI()
app.include_router(socket_router)

@app.on_event("startup")
async def start_polling():
    db = await anext(get_db())
    asyncio.create_task(poll_and_broadcast(db))
