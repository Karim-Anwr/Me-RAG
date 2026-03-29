# src/routes/data.py

from urllib import request

from fastapi import FastAPI, APIRouter, Depends , UploadFile ,status ,Request
from fastapi.responses import JSONResponse
import os
from models.enums.ResponseEnums import ResponseSignal
from models.enums.DataBaseEnum import DataBaseEnum


from helpers.config import get_settings , Settings
#from controllers import DataController , ProcessController ,ProjectController
from controllers.DataController import DataController
from controllers.ProjectController import ProjectController
from controllers.ProcessController import ProcessController
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
import aiofiles
from .schemas.data import ProcessRequest
from models.db_schemes import DataChunk


import logging
logging = logging.getLogger("uvicorn.error")


data_router = APIRouter(
    prefix="/data",
    tags=["data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(request: Request, project_id: str, file: UploadFile, app_settings : Settings= Depends(get_settings)):

    project_model = ProjectModel(db_client=request.app.state.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)

    data_controller = DataController()
    is_valid, message = data_controller.validate_uploaded_file(file=file)
    if not is_valid:
        return JSONResponse(content={"message": message}, status_code=status.HTTP_400_BAD_REQUEST)

    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path, file_id = data_controller.generate_unique_filepath(orig_file_name=file.filename, project_id=project_id)
 
    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:

        logging.error(f"Error saving file: {str(e)}")

        return JSONResponse(content={"message": f"{ResponseSignal.FILE_UPLOAD_FAILED.value} - {str(e)}"}, status_code=status.HTTP_400_BAD_REQUEST)

    return JSONResponse(content={"message": ResponseSignal.FILE_UPLOAD_SUCCESS.value, "file_id": file_id }, status_code=status.HTTP_200_OK) 


@data_router.post("/process/{project_id}")
async def process_endpoint(request: Request, project_id: str, process_request: ProcessRequest):
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size

    project_model = ProjectModel(db_client=request.app.state.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)

    process_controller = ProcessController(project_id=project_id)

    file_content = process_controller.get_file_content(file_id=file_id)
    file_chunks = process_controller.process_file_content(file_content=file_content, file_id=file_id, chunk_size=chunk_size, overlap_size=overlap_size) 
    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(content={"message": ResponseSignal.FILE_PROCESSING_FAILED.value}, status_code=status.HTTP_400_BAD_REQUEST)
    file_chunk_records = [DataChunk(chunk_text=chunk.page_content , chunk_metadata=chunk.metadata, chunk_order=i+1, chunk_project_id=project.id) for i ,chunk in enumerate(file_chunks)]
    chunk_model = ChunkModel(db_client=request.app.state.db_client)
    await chunk_model.insert_many_chunks(chunks=file_chunk_records)