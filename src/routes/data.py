"""This module defines FastAPI routes for handling data-related operations in the MiniRAG system."""
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

# ====================
# Router Configuration
# ====================
data_router = APIRouter(
    prefix="/api/v1/data",      # All endpoints here start with /api/v1/data
    tags=["api_v1", "data"],    # Group name for Swagger UI
)

# ======
# GET /
# ======
@data_router.get("/")
async def welcome_data():
    """
    Root endpoint for /api/v1/data.

    Returns:
        str: A simple welcome message for testing.
    """
    return "welcome data"

# ===========================
# POST /upload/{project_id}
# ===========================
@data_router.post("/upload/{project_id}")
async def upload_data(request: Request, project_id: int, file: UploadFile = None, 
                      app_settings: Settings = Depends(get_settings)):
    """
    Upload a file and store it as an Asset under a specific project.

    Steps:
    1. Validate file type and size.
    2. Save the file asynchronously to disk.
    3. Register the file as an Asset in the database.
    4. Return a success signal and file_id.

    Args:
        request (Request): FastAPI request object containing app context.
        project_id (int): ID of the project to associate the file with.
        file (UploadFile): Uploaded file object from the client.
        app_settings (Settings): Application configuration settings.

    Returns:
        JSONResponse: Upload result, including `file_id` if successful.
    """
    
    # Ensure project exists or create one
    print("project_id:", project_id)
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)

    # Validate uploaded file
    data_controller = DataController()
    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "Signal": result_signal
                } 
        )

    # project_dir_path = ProjectController().get_project_path(project_id=project_id)

    # Generate unique file path using DataController utility
    file_path, file_id = data_controller.generate_unique_file_path(
        original_filename=file.filename,
        project_id=project_id
    )
    print("file_path:", file_path)

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

    # store assets in database
    asset_model = await AssetModel.create_instance(db_client=request.app.db_client)
    asset_resource = Asset(
        asset_project_id=project.project_id,  
        asset_type=AssetTypeEnum.FILE.value,
        asset_name=file_id,
        asset_size=os.path.getsize(file_path)
    )
    print("asset_resource:", asset_resource)
    asset_record = await asset_model.create_asset(asset=asset_resource)

    # Success response    
    return JSONResponse(
        # status_code=status.HTTP_200_OK, # status code 200 by default
        content={
            "Signal": ResponseSignal.FILE_UPLOADED_SUCCESSFULLY.value,
            "file_id": str(asset_record.asset_id)
        }
    )

# ===========================
# POST /process/{project_id}
# ===========================
@data_router.post("/process/{project_id}")
async def process_endpoint(request: Request, project_id: int, process_request: ProcessRequest):
    """
    Process uploaded files and generate text chunks for RAG indexing.

    Steps:
    1. Fetch all assets (or a specific one if file_id provided).
    2. Read and split file content into overlapping text chunks.
    3. Store chunks in the database.
    4. Optionally reset existing chunks and vector collections.

    Args:
        request (Request): FastAPI request context.
        project_id (int): ID of the project to process.
        process_request (ProcessRequest): Configuration for chunk size, overlap, etc.

    Returns:
        JSONResponse: Processing result summary.
    """

    # file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset

    # Ensure project exists
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    print("project_id processss:", project_id)
    project = await project_model.get_project_or_create_one(project_id=project_id)

    # Initialize NLP and Asset controllers
    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
        template_parser=request.app.template_parser
    )
    asset_model = await AssetModel.create_instance(db_client=request.app.db_client)

    # Get relevant assets (single file or all files)
    project_file_ids = {}
    if process_request.file_id:
        # get a specific file with file_id
        asset_record = await asset_model.get_asset_record(
            asset_project_id=project.project_id,
            asset_name=process_request.file_id
        )
        print("asset_record:", asset_record.asset_name, asset_record.asset_project_id)

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
        # get all files belonging to the project
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
    print("project_file_ids:", project_file_ids)
    # Process each file
    process_controller = ProcessController(project_id=project_id)
    chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)

    num_recordes = 0
    num_files = 0

    # Optional reset: clear old chunks + vector collection
    if do_reset == 1:
        collection_name = nlp_controller.create_collection_name(project_id=project.project_id)

        _ = await request.app.vectordb_client.delete_collection(collection_name=collection_name)

        _ = await chunk_model.delete_chunks_by_project_id(project_id=project.project_id)

    for asset_id, file_id in project_file_ids.items(): # file_id is asset_name in Asset model

        file_content = process_controller.get_file_content(file_id=file_id)

        if file_content is None:
            logger.error(f"Error while processing file: {file_id}")
            continue

        # Generate text chunks
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
        
        # Convert to objects
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

@data_router.post("/delete/{project_id}")
async def delete_project_data(request: Request, project_id: int):

    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.check_project_exist(project_id=project_id)

    if not project:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "Signal": ResponseSignal.PROJECT_NOT_FOUND.value
            }
        )

    chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)
    asset_model = await AssetModel.create_instance(db_client=request.app.db_client)

    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client= request.app.generation_client, 
        embedding_client = request.app.embedding_client,
        template_parser=request.app.template_parser
    )

    # delete vector db collection
    collection_name = nlp_controller.create_collection_name(project_id=project.project_id)
    _ = await request.app.vectordb_client.delete_collection(collection_name=collection_name)

    # delete chunks
    deleted_chunks = await chunk_model.delete_chunks_by_project_id(project_id=project.project_id)

    # delete assets
    deleted_assets = await asset_model.delete_assets_by_project_id(project_id=project.project_id)

    # delete project record
    _ = await project_model.delete_project_by_id(project_id=project.project_id)

    return JSONResponse(
        content={
            "Signal": ResponseSignal.PROJECT_DATA_DELETED.value,
            "deleted_chunks": deleted_chunks,
            "deleted_assets": deleted_assets
        }
    )



# to run python -m routes.data
