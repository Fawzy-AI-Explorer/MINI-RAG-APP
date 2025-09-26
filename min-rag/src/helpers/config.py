from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Configuration settings for the application.
    Put here all var exist in .env file
    """

    APP_NAME: str 
    APP_VERSION: str
    API: str

    FILE_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    MONGODB_URL:str
    MONGODB_DATABASE:str

    GENERATION_BACKEND:str
    EMBEDDING_BACKEND:str

    OPENAI_API_KEY:str
    OPENAI_API_URL:str
    COHERE_API_KEY:str

    GENERATION_MODEL_ID:str
    EMBEDDING_MODEL_ID:str
    EMBEDDING_MODEL_SIZE:int

    iINPUT_DEFAULT_MAX_CHARACTERS:int
    GENERATION_DEFAULT_MAX_TOKENS:int
    GENERATION_DEFAULT_TEMPERATURE:float

    VECTOR_DB_BACKEND:str
    VECTOR_DB_PATH:str
    VECTOR_DB_DISTANCE_METHOD:str

    PRIMARY_LANGUAGE:str
    DEFAULT_LANGUAGE:str = "en"

    class Config:
        env_file = r"E:\DATA SCIENCE\MINI-RAG-APP\min-rag\.env" # r"/mnt/e/DATA SCIENCE/MINI-RAG-APP/min-rag/.env"

def get_settings():

    return Settings()

if __name__ == "__main__":
    settings = get_settings()
    print(settings.APP_NAME)
    print(settings.APP_VERSION)
    print(settings.API)
    print(settings.FILE_ALLOWED_TYPES)
    print(settings.FILE_MAX_SIZE)


# min-rag/src/
# to run : python -m helpers.config