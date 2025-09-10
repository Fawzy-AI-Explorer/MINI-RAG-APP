from fastapi import FastAPI, APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
import aiofiles
import logging
import os

from src.helpers.config import get_settings, Settings

from src.controllers.DataController import DataController
from src.controllers.ProjectController import ProjectController
from src.controllers.ProcesController import ProcessController

from src.models.db_schemes.data_chunk import DataChunk
from src.models.db_schemes.assest import Asset

from src.models.ProjectModel import ProjectModel
from src.models.ChunckModel import ChunckModel
from src.models.AssetModel import AssetModel

from src.models.enums.ResponseEnums import ResponseSignal
from src.models.enums.AssetTypeEnums import AssetTypeEnum
from src.routes.schemas.data import ProcessRequest




logger = logging.getLogger("uvicorn.error")
data_router = APIRouter(
    prefix="/api/v1/data",      # Base path for all routes in this router  || before the decorator put /api/v1
    tags=["api_v1", "data"],    # Tags for grouping in Swagger UI
)

@data_router.get("/")
async def welcome_data():
    return "welcome data"

@data_router.post("/upload/{project_id}")
async def upload_data(request: Request, project_id: str, file: UploadFile = None, 
                      app_settings: Settings = Depends(get_settings)):
    
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)



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

    # project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path, file_id = data_controller.generate_unique_file_path(
        original_filename=file.filename,
        project_id=project_id
    )

    try:
        # it is not efficient to read the whole file at once (save it in temporary), especially for large files and many users.
        # Instead, read and write the file in chunks.
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

    # store the assets into database
    asset_model = await AssetModel.create_instance(db_client=request.app.db_client)
    asset_resource = Asset(
        asset_projec_id=project.id,
        asset_type=AssetTypeEnum.FILE.value,
        asset_name=file_id,
        asset_size=os.path.getsize(file_path)
    )

    asset_record = await asset_model.create_asset(asset=asset_resource)

    
    return JSONResponse(
        # status_code=status.HTTP_200_OK, # status code 200 by default
        content={
            "Signal": ResponseSignal.FILE_UPLOADED_SUCCESSFULLY.value,
            "file_id": str(asset_record.id)
        }
    )

@data_router.post("/process/{project_id}")
async def process_endpoint(request: Request, project_id: str, process_request: ProcessRequest):

    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset


    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)

        # You can add validation for chunk_size and overlap_size if needed
    process_controller = ProcessController(project_id=project_id)
    file_content = process_controller.get_file_content(file_id=file_id)
    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )

    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "Signal": ResponseSignal.FILE_PROCESSING_FAILED.value
                } 
        )
    
    file_chunks_records = [
        DataChunk(
            chunck_text=chunk.page_content,
            chunck_matadata=chunk.metadata,
            chunck_order= i+1,
            chunck_projec_id= project.id
        )
        for i, chunk in enumerate(file_chunks)
    ]

    chunck_model = await ChunckModel.create_instance(db_client=request.app.db_client)

    if do_reset == 1:
        _ = await chunck_model.delete_chunks_by_project_id(project_id=project.id)

    num_recordes = await chunck_model.insert_many_chunks(
        chunks=file_chunks_records,
        batch_size=100
    )

    return JSONResponse(
        content={
            "Signal": ResponseSignal.FILE_PROCESSED_SUCCESSFULLY.value,
            "inserted_chunks": num_recordes
        }
    )
# to run python -m routes.data
