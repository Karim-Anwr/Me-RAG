# src/models/ProjectModel.py

# src/models/ProjectModel.py
from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum 

class ProjectModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.PROJECTS_COLLECTION.value]

    async def create_project(self, project: Project):
        project_dict = project.dict(by_alias=True, exclude_unset=True)
        result = await self.collection.insert_one(project_dict)
        project._id = result.inserted_id
        return project
    
    async def get_project_or_create_one(self, project_id: str):
        project = await self.collection.find_one({"Project_id": project_id})
        if project:
            return Project(**project)
        else:
            new_project = Project(Project_id=project_id, name="Default Name", description="Default Description")
            return await self.create_project(new_project)
        
    async def get_all_projects(self , page: int = 1, page_size: int = 10):
        total_documents = await self.collection.count_documents({}) 
        total_pages = (total_documents + page_size - 1) // page_size
        
        cursor = self.collection.find().skip((page - 1) * page_size).limit(page_size)
        projects = [Project(**doc) async for doc in cursor]
        return {
            "projects": projects,
            "total_pages": total_pages,
            "current_page": page
        }


    