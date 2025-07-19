from fastapi import FastAPI, APIRouter
import os

base_router = APIRouter(
    prefix="/api/v1",  # Base path for all routes in this router  || before the decorator put /api/v1
    tags=["NLP"],      # Tags for grouping in Swagger UI
)

@base_router.get("/") 
async def welocome():
    app_name = os.getenv("APP_NAME")
    app_version = os.getenv("APP_VERSION")
    return{
    "message": "Welcome to the FastAPI application!{app_name} - {app_version}".format(app_name=app_name, app_version=app_version)
    }



