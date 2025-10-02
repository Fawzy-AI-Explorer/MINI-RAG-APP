from fastapi import FastAPI, APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
import aiofiles
import logging
import os

from src.helpers.config import get_settings, Settings

from src.controllers.DataController import DataController
from src.controllers.NLPController import NLPController
from src.controllers.ProcesController import ProcessController

from src.models.db_schemes import Asset, DataChunk

from src.models.ProjectModel import ProjectModel
from src.models.ChunkModel import ChunkModel
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
async def upload_data(request: Request, project_id: int, file: UploadFile = None, 
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
        asset_project_id=project.project_id,  
        asset_type=AssetTypeEnum.FILE.value,
        asset_name=file_id,
        asset_size=os.path.getsize(file_path)
    )

    asset_record = await asset_model.create_asset(asset=asset_resource)

    
    return JSONResponse(
        # status_code=status.HTTP_200_OK, # status code 200 by default
        content={
            "Signal": ResponseSignal.FILE_UPLOADED_SUCCESSFULLY.value,
            "file_id": str(asset_record.asset_id)
        }
    )

@data_router.post("/process/{project_id}")
async def process_endpoint(request: Request, project_id: int, process_request: ProcessRequest):

    # file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset


    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)
    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
        template_parser=request.app.template_parser
    )
    asset_model = await AssetModel.create_instance(db_client=request.app.db_client)


    project_file_ids = {}
    if process_request.file_id:
        asset_record = await asset_model.get_asset_record(
            asset_project_id=project.project_id,
            asset_name=process_request.file_id
        )

        if asset_record is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "Signal": ResponseSignal.FILE_ID_ERROR.value
                    } 
            )
        
        project_file_ids = {
            asset_record.asset_id : asset_record.asset_name
            }
    else:
        project_files = await asset_model.get_all_project_assets(
            asset_project_id=project.project_id,
            asset_type=AssetTypeEnum.FILE.value
        )
        project_file_ids = {
            record.asset_id : record.asset_name
            for record in project_files
        }

    if len(project_file_ids) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "Signal": ResponseSignal.NO_FILE_ERROR.value
                } 
        )
    

    process_controller = ProcessController(project_id=project_id)
    chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)

    num_recordes = 0
    num_files = 0

    if do_reset == 1:
        collection_name = nlp_controller.create_collection_name(project_id=project.project_id)

        _ = await request.app.vectordb_client.delete_collection(collection_name=collection_name)

        _ = await chunk_model.delete_chunks_by_project_id(project_id=project.project_id)

    for asset_id, file_id in project_file_ids.items(): # file_id is asset_name in Asset model

        file_content = process_controller.get_file_content(file_id=file_id)

        if file_content is None:
            logger.error(f"Error while processing file: {file_id}")
            continue

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
                chunk_text=chunk.page_content,
                chunk_metadata=chunk.metadata,
                chunk_order= i+1,
                chunk_project_id= project.project_id,
                chunk_asset_id=asset_id
            )
            for i, chunk in enumerate(file_chunks)
        ]

        

        num_recordes += await chunk_model.insert_many_chunks(chunks=file_chunks_records)
        num_files +=1

    return JSONResponse(
        content={
            "Signal": ResponseSignal.FILE_PROCESSED_SUCCESSFULLY.value,
            "inserted_chunks": num_recordes,
            "processed_files": num_files
        }
    )
# to run python -m routes.data
