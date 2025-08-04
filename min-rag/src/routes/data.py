from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
import os
from src.helpers.config import get_settings, Settings
from src.controllers.DataController import DataController
from src.controllers.ProjectController import ProjectController
import aiofiles
from src.models.enums.ResponseEnums import ResponseSignal
import logging


print("🚀 data.py loaded")

logger = logging.getLogger("uvicorn.error")
data_router = APIRouter(
    prefix="/api/v1/data",  # Base path for all routes in this router  || before the decorator put /api/v1
    tags=["api_v1", "data"],    # Tags for grouping in Swagger UI
)

@data_router.get("/")
async def welcome_data():
    return "welcome data"

@data_router.get("/upload/{project_id}")
# async def upload_data(project_id: str, ):
#     return 555
async def upload_data(project_id: str, file: UploadFile = None, 
                      app_settings: Settings = Depends(get_settings)):
    
    data_controller = DataController()
    # Validate file type and size
    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "Signal": result_signal
                } 
        )

    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path, file_id = data_controller.generate_unique_file_path(
        original_filename=file.filename,
        project_id=project_id
    )

    try:

        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error while Uploading file: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "Signal": ResponseSignal.FILE_UPLOADED_FAILED.value
                } 
        )

    
    return JSONResponse(
        content={
            "Signal": ResponseSignal.FILE_UPLOADED_SUCCESSFULLY.value,
            "file_path": file_path, 
            "file_id": file_id
        }
    )
    

    # return {"valid?" : is_valid, 
    #         "Signal": result_signal}

    
    

# to run python -m routes.data