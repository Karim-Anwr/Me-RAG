# src/models/db_schemes/Project.py

from typing import Optional

from pydantic import BaseModel, Field , validator
from bson.objectid import ObjectId

class Project(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    Project_id : str = Field(..., min_length=1)
    name: str
    description: str

    @validator('Project_id')
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError('Project_id must contain only alphanumeric characters')
        return value
    
    class Config:
        arbitrary_types_allowed = True
