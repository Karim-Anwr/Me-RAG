# src/controllers/DataController.py

from fileinput import filename
import os
import uuid

from .BaseController import  BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models.enums import ResponseSignal
import re

class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def validate_uploaded_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        
        if file.size > self.app_settings.FILE_MAX_SIZE:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
    
        return True, ResponseSignal.FILE_VALIDATION_SUCCESS.value


    def generate_unique_filename(self, orig_file_name: str , project_id: str):
        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)

        cleaned_filename = self.get_clean_filename(orig_file_name=orig_file_name)

        new_file_path = os.path.join(project_path, f"{random_key}_{cleaned_filename}")

        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(project_path, f"{random_key}_{cleaned_filename}")

        return new_file_path

    def get_clean_filename(self, orig_file_name: str):
        filename = orig_file_name.replace(" ", "_")
        cleaned_filename = re.sub(r'[^\w.]', '', filename)

        if not cleaned_filename:
            cleaned_filename = "file"

        return cleaned_filename
