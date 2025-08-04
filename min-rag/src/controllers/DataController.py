from src.controllers.BaseController import BaseController
from src.controllers.ProjectController import ProjectController
from fastapi import UploadFile
from src.models.enums.ResponseEnums import ResponseSignal
import re
import os

class DataController(BaseController):
    
    def __init__(self):
        super().__init__()  # Initialize BaseController to access app settings
        self.size_scale =  1024 * 1024  # Convert MB to bytes

    def validate_uploaded_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseSignal.FILE_VALIDATE_SUCCESS.value
        
        return True, ResponseSignal.FILE_VALIDATE_SUCCESS.value

    def generate_unique_file_path(self, original_filename: str, project_id: str):
    
        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)
        cleaned_file_name = self.get_clean_file_name(original_filename= original_filename)

        new_file_path = os.path.join(project_path, f"{random_key}_{cleaned_file_name}")

        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(project_path, f"{random_key}_{cleaned_file_name}")
        
        return new_file_path, f"{random_key}_{cleaned_file_name}"

    def get_clean_file_name(self, original_filename: str):

        # Remove any special characters and keep only alphanumeric characters, underscores, and dots
        cleaned_file_name = re.sub(r'[^\w]', '', original_filename)
        cleaned_file_name = cleaned_file_name.replace(" ", "_")  # Replace spaces with underscores

        return cleaned_file_name

         

        pass
        

if __name__ == "__main__":
    print("DataController initialized with app settings:")
    controller = DataController()
    print(controller.get_app_settings())


# to run python -m controllers.DataController
