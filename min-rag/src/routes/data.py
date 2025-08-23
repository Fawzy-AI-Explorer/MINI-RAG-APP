from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
import os
from src.helpers.config import get_settings, Settings
from src.controllers.DataController import DataController
from src.controllers.ProjectController import ProjectController
import aiofiles
from src.models.enums.ResponseEnums import ResponseSignal
import logging
from src.routes.schemas.data import ProcessRequest

print(" data.py loaded")

logger = logging.getLogger("uvicorn.error")
data_router = APIRouter(
    prefix="/api/v1/data",      # Base path for all routes in this router  || before the decorator put /api/v1
    tags=["api_v1", "data"],    # Tags for grouping in Swagger UI
)

@data_router.get("/")
async def welcome_data():
    return "welcome data"

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, 
                      file: UploadFile = None, 
                      app_settings: Settings = Depends(get_settings)):
    
    data_controller = DataController()
    # Validate file type and size
    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, # if not success return 400 else 200
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
        print("Uploading file to:", file_path)

        # it is not efficient to read the whole file at once (save it in temporary), especially for large files and many users.
        # Instead, read and write the file in chunks.
        async with aiofiles.open(file_path, "wb") as f:
            print("file opened")
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                print("writing chunk")
                await f.write(chunk)
        print("File upload completed.")
    except Exception as e:
        logger.error(f"Error while Uploading file: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "Signal": ResponseSignal.FILE_UPLOADED_FAILED.value
                } 
        )

    
    return JSONResponse(
        # status_code=status.HTTP_200_OK, # status code 200 by default
        content={
            "Signal": ResponseSignal.FILE_UPLOADED_SUCCESSFULLY.value,
            # "file_path": file_path, 
            "file_id": file_id
        }
    )




@data_router.post("/process/{project_id}")
async def process_endpoint(project_id: str, process_request: ProcessRequest):
    
    file_id = process_request.file_id
    return file_id



    
    

# to run python -m routes.data