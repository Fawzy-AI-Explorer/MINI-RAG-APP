# from fastapi import FastAPI

# app = FastAPI()

# ============================== Swagger ==============================
# http://127.0.0.1:8000/docs || to see the API documentation (FastAPI auto-generates)

# When you create an API, Swagger helps you:
# Describe your API: What endpoints exist, what parameters they need, what responses they return.
# Test your API: Through an interactive web interface.
# Share your API: Other developers can understand and use it easily.
#================================================================================================================

# ============================== postman ==============================
# Postman is a popular API development tool used to:

# Send requests to APIs (GET, POST, PUT, DELETE...)
# Test API responses interactively
# Automate testing
# Organize APIs into collections
# Document APIs for sharing with teams
# Mock servers, generate code snippets, etc.

# collection from top right corner
# create a new collection  (U can Rename it)
# on variables tab, you can add variables that can be used in your requests (put the original api URL and set the variable name to any_name)
# from the 3 dots on the right side of the collection, add a new request
# set the URL to {{any_name}}/welcome  || click send

# @app.get("/welcome") # decorator to define a route when put /welcome after the base URL call this function
# # API routes (GET, POST, PUT, DELETE...)
# def welocome():
#     return{
#     "message": "Wel ome to the FastAPI application!"
#     }






from fastapi import FastAPI
from src.routes.base import base_router
from src.routes.data import data_router
from src.routes.nlp import nlp_router
from src.helpers.config import get_settings
from src.stores import LLMProviderFactory
from src.stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory
from src.stores.llm.templates.template_parser import TemplateParser
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

app = FastAPI()

@app.on_event("startup")
async def startup_span():
    settings = get_settings()

    postgres_conn = f"postgresql+asyncpg://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_MAIN_DATABASE}"
    app.db_engine = create_async_engine(postgres_conn)
    app.db_client = sessionmaker(
        app.db_engine, class_=AsyncSession, expire_on_commit=False
    )

    llm_provider_factory = LLMProviderFactory(settings)
    vectordb_provider_factory = VectorDBProviderFactory(settings)

    app.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID)

    app.embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID, 
                                             embedding_size=settings.EMBEDDING_MODEL_SIZE)
    
    app.vectordb_client = vectordb_provider_factory.create(provider=settings.VECTOR_DB_BACKEND)
    app.vectordb_client.connect()

    app.templat_parser = TemplateParser(
        language=settings.PRIMARY_LANGUAGE,
        defaulat_language=settings.DEFAULT_LANGUAGE
    )

@app.on_event("shutdown")
async def shutdown_span():
    app.db_engine.dispose() # close the connection when app shuts down
    app.vectordb_client.disconnect()

# app.router.lifespan.on_startup.append(startup_db_client)
# app.router.lifespan.on_shutdown.append(shutdown_db_client)

app.include_router(data_router)
app.include_router(base_router)
app.include_router(nlp_router)

# print("✅ Routes:")
# for route in app.routes:
#     print(route.path, route.name)







# ======================
# python3 --version
# sudo apt update
# sudo apt install python3.12-venv -y  (Same Version as your python version)
# python3 -m venv .venv
# source .venv/bin/activate
# pip list
# sudo apt install python3-pip  (To install pip if not installed)
# sudo apt install uvicorn
# pip install fastapi uvicorn
# ======================

# Run Docker : sudo docker compose up

# This for local testing only Not for production
# stop docker   ===>  sudo docker stop $(sudo docker ps -aq)
# remove docker ===>  sudo docker rm $(sudo docker ps -aq)
# remove images ===>  sudo docker rmi $(sudo docker images -q)
# remove volumes ===>  sudo docker volume rm $(sudo docker volume ls -q)
# clean up all unused docker objects ===>  sudo docker system prune --all

# uvicorn main:app --reload
# sh scripts/run_app.sh
