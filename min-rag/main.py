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
from src.utils.metrics import setup_metrics
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware

app = FastAPI()
setup_metrics(app)

@app.on_event("startup")
async def startup_span():
    settings = get_settings()

    postgres_conn = f"postgresql+asyncpg://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_MAIN_DATABASE}"
    app.db_engine = create_async_engine(postgres_conn)
    app.db_client = sessionmaker(
        app.db_engine, class_=AsyncSession, expire_on_commit=False
    )

    llm_provider_factory = LLMProviderFactory(settings)
    vectordb_provider_factory = VectorDBProviderFactory(config = settings, db_client=app.db_client)

    app.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID)

    app.embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID, 
                                             embedding_size=settings.EMBEDDING_MODEL_SIZE)
    
    app.vectordb_client = vectordb_provider_factory.create(provider=settings.VECTOR_DB_BACKEND)
    await app.vectordb_client.connect()

    app.template_parser = TemplateParser(
        language=settings.PRIMARY_LANGUAGE,
        defaulat_language=settings.DEFAULT_LANGUAGE
    )

@app.on_event("shutdown")
async def shutdown_span():
    app.db_engine.dispose() # close the connection when app shuts down
    await app.vectordb_client.disconnect()


# --- CORS Middleware Configuration ---
# This allows your frontend (the HTML file) to make requests to this backend server.
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "null",  # Allow requests from local files (file://)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, OPTIONS)
    allow_headers=["*"],  # Allows all headers
)
# -----------------------------------


app.include_router(data_router)
app.include_router(base_router)
app.include_router(nlp_router)

# print("Routes:")
# for route in app.routes:
#     print(    route.path, route.name)


# uvicorn main:app --reload
# sh scripts/run_app.sh
