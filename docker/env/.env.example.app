APP_NAME="mini-rag-app"
APP_VERSION="0.1.0"

FILE_ALLOWED_TYPES=["text/plain", "application/pdf"]
FILE_MAX_SIZE=10
FILE_DEFAULT_CHUNK_SIZE=512000 # 512 KB

POSTGRES_USERNAME=""  
POSTGRES_PASSWORD=""
POSTGRES_HOST=""
POSTGRES_PORT=
POSTGRES_MAIN_DATABASE=""

# ================================ LLM config =================================
GENERATION_BACKEND = ""
EMBEDDING_BACKEND = ""

OPENAI_API_KEY="sk-........"
OPENAI_API_URL=""
COHERE_API_KEY="pT............"

GENERATION_MODEL_ID_LITERAL=["..........", "....", "...."]
GENERATION_MODEL_ID="...."        
EMBEDDING_MODEL_ID="...."   
EMBEDDING_MODEL_SIZE=

iINPUT_DEFAULT_MAX_CHARACTERS=
GENERATION_DEFAULT_MAX_TOKENS=
GENERATION_DEFAULT_TEMPERATURE=

# ================================= VectorDB config ================================
VECTOR_DB_BACKEND_LITERAL=["", ""]
VECTOR_DB_BACKEND=""
VECTOR_DB_PATH=""
VECTOR_DB_DISTANCE_METHOD=""
VECTOR_DB_PGVEC_INDEX_THRESHOLD=

# ================================ Templates config=================================
PRIMARY_LANGUAGE=""
DEFAULT_LANGUAGE=""
