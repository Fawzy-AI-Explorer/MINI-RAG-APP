# from helpers.config import get_settings, Settings
from src.helpers.config import get_settings, Settings
import os
import random
import string


class BaseController:

    def __init__(self):

        self.app_settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  
        self.file_dir = os.path.join(self.base_dir, "assets", "files") # To store uploaded files

        self.db_dir = os.path.join(self.base_dir, "assets", "database") # To store vector DB files

        # print(f"__file__ :  {__file__}") # E:\DATA SCIENCE\MINI-RAG-APP\min-rag\src\controllers\BaseController.py
        # print(f"os.path.dirname(__file__), {os.path.dirname(__file__)}") # E:\DATA SCIENCE\MINI-RAG-APP\min-rag\src\controllers
        # print(f"self.base_dir : {self.base_dir}") # E:\DATA SCIENCE\MINI-RAG-APP\min-rag\src
        # print(f"self.file_dir : {self.file_dir}") # E:\DATA SCIENCE\MINI-RAG-APP\min-rag\src\assets\files      

    def generate_random_string(self, length: int = 12) -> str:
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def get_app_settings(self) -> Settings:
        return self.app_settings
    
    def get_database_path(self, db_name):
        database_path = os.path.join(self.db_dir, db_name)
        if not os.path.exists(database_path):
            os.makedirs(database_path, exist_ok=True)
        return database_path


if __name__ == "__main__":
    print("BaseController initialized with app settings:")
    # controller = BaseController()
    # print(controller.get_app_settings())

#  cd min-rag/src/
# to run python -m controllers.BaseController
