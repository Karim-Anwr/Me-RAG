# src/routes/data.py

from fastapi import FastAPI, APIRouter, Depends , UploadFile ,status
from fastapi.responses import JSONResponse
import os
from models.enums import ResponseSignal
from helpers.config import get_settings , Settings
from controllers.DataController import DataController
from controllers.ProjectController import ProjectController
import aiofiles

import logging
logging = logging.getLogger("uvicorn.error")


data_router = APIRouter(
    prefix="/data",
    tags=["data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile, app_settings : Settings= Depends(get_settings)):

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

    return JSONResponse(content={"message": ResponseSignal.FILE_UPLOAD_SUCCESS.value, "file_id": file_id}) 