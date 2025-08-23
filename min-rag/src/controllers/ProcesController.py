from src.controllers.BaseController import BaseController
from src.controllers.ProjectController import ProjectController
# from fastapi import UploadFile
from src.models.enums.ProcessingEnums import ProcessingEnums
# import re
import os
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader

class DataController(BaseController):
    
    def __init__(self, project_id: str):
        super().__init__()  # Initialize BaseController to access app settings

        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    def get_file_extension(self, file_id: str):
        
        return os.path.splitext(file_id)[-1]

    def get_file_loader(self, file_id: str, file_path: str):
        
        file_extension = self.get_file_extension(file_id=file_id)

        if file_extension == ProcessingEnums.PDF.value:
            return PyMuPDFLoader(file_path)
    
        elif file_extension == ProcessingEnums.TXT.value:
            return TextLoader(file_path)
        else:
            None 