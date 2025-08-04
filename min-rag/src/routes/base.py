from fastapi import FastAPI, APIRouter, Depends
import os
from src.helpers.config import get_settings, Settings
print("🚀 base.py loaded")
base_router = APIRouter(
    prefix="/api/v1",  # Base path for all routes in this router  || before the decorator put /api/v1
    tags=["api_v1"],      # Tags for grouping in Swagger UI
)

@base_router.get("/") 
async def welocome(app_settings: Settings=Depends(get_settings)):
    # app_settings = get_settings()
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    return{
        "app_name": app_name,
        "app_version": app_version,    
     }

@base_router.get("/welcome") 
async def welocomeee():
    return{"message": "Welcome to the FastAPI application!"}



# to run python -m src.routes.base import base_router