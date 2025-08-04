# from helpers.config import get_settings, Settings
from src.helpers.config import get_settings, Settings
import os
import random
import string


class BaseController:

    def __init__(self):

        self.app_settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.file_dir = os.path.join(self.base_dir, "assets", "files")

    def generate_random_string(self, length: int = 12) -> str:
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def get_app_settings(self) -> Settings:
        return self.app_settings


if __name__ == "__main__":
    print("BaseController initialized with app settings:")
    controller = BaseController()
    print(controller.get_app_settings())

#  cd min-rag/src/
# to run python -m controllers.BaseController
