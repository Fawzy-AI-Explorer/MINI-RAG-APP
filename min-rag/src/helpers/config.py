from pydantic_settings import BaseSettings, SettingsConfigDict, YamlConfigSettingsSource
from pathlib import Path
from typing import List

class Settings(BaseSettings):
    """
    Configuration settings for the application.
    Put here all var exist in .env file
    """

    APP_NAME: str 
    APP_VERSION: str
    API: str

    FILE_ALLOWED_TYPES: List[str]
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_MAIN_DATABASE: str

    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    OPENAI_API_KEY: str
    OPENAI_API_URL: str
    COHERE_API_KEY: str

    GENERATION_MODEL_ID_LITERAL: List[str]
    GENERATION_MODEL_ID: str
    EMBEDDING_MODEL_ID: str
    EMBEDDING_MODEL_SIZE: int

    iINPUT_DEFAULT_MAX_CHARACTERS: int
    GENERATION_DEFAULT_MAX_TOKENS: int
    GENERATION_DEFAULT_TEMPERATURE: float

    VECTOR_DB_BACKEND_LITERAL: List[str]
    VECTOR_DB_BACKEND: str
    VECTOR_DB_PATH: str
    VECTOR_DB_DISTANCE_METHOD: str
    VECTOR_DB_PGVEC_INDEX_THRESHOLD: int = 100

    PRIMARY_LANGUAGE: str
    DEFAULT_LANGUAGE: str = "en"

    # class Config:
    #     # env_file = r"\mnt\E:\DATA SCIENCE\MINI-RAG-APP\min-rag\.env" # r"/mnt/e/DATA SCIENCE/MINI-RAG-APP/min-rag/.env"
    #     env_file = r"/mnt/e/DATA SCIENCE/MINI-RAG-APP/min-rag/.env"

    model_config = SettingsConfigDict(env_file=r".env", env_file_encoding="utf-8")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        return (
            init_settings,  # kwargs passed directly to Settings()
            env_settings,  # Environment variables
            dotenv_settings,  # .env file
            YamlConfigSettingsSource(
                settings_cls,
                yaml_file=Path(r"config\config.yaml"),
                yaml_file_encoding="utf-8",
            ),  # YAML file
            file_secret_settings,  # Secrets from files
        )


def get_settings():

    return Settings()

if __name__ == "__main__":
    settings = get_settings()
    print(settings.APP_NAME)
    print(settings.APP_VERSION)
    print(settings.API)
    print(settings.FILE_ALLOWED_TYPES)
    print(settings.FILE_MAX_SIZE)


# to run : python -m helpers.config
