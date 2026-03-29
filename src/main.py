from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.state.db_client = AsyncIOMotorClient(settings.MONOGODB_URI)[settings.MONGODB_DATABASE]
    print(" Mongo connected")

@app.on_event("shutdown")
async def shutdown_db_client():
    app.state.db_client.client.close()
    print(" Mongo disconnected")

app.include_router(base.base_router)
app.include_router(data.data_router)