<!--- Badges -->
[![GitHub stars](https://img.shields.io/github/stars/Fawzy-AI-Explorer/MINI-RAG-APP?style=social)](https://github.com/Fawzy-AI-Explorer/MINI-RAG-APP)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

# MINI-RAG-APP 🚀

A minimal Retrieval-Augmented Generation (RAG) reference implementation built with FastAPI, pluggable LLM/embedding providers, and vector databases (pgvector / Qdrant). This project is designed to help you ingest documents, chunk them, index into a vector store, and run RAG-style question answering or generation pipelines.

Whether you want to run it locally with uvicorn or in containers via Docker Compose, this README will guide you through setup, configuration, and examples to get you productive quickly. Friendly, approachable, and ready for customization. 🛠️

## Features ✨

- FastAPI backend with asynchronous startup/shutdown hooks
- Pluggable LLM providers and embedding backends (OpenAI, Cohere, local providers via factory pattern)
- Supports multiple vector databases: PostgreSQL + pgvector and Qdrant
- File upload endpoint with streaming-safe write (aiofiles)
- Document processing pipeline: chunking, overlap control, chunk storage and indexing
- Monitoring endpoints (Prometheus + Grafana integration via Docker Compose)
- Docker Compose stack for quick local deployments (FastAPI, Postgres/pgvector, Qdrant, Prometheus, Grafana)

## Project structure 📁

Complete repository layout (based on the current workspace):

```
MINI-RAG-APP/
├── .env
├── .env.example
├── .gitignore
├── main.py                      # FastAPI entrypoint & lifecycle hooks
├── pyproject.toml               # package metadata
├── README.md
├── requirements.txt             # pinned deps for quick install
├── .vscode/
├── assets/                      # persisted data and sample files
│   ├── .gitignore
│   ├── .gitkeep
│   ├── database/
│   └── files/
├── config/
│   └── config.yaml
├── docker/                      # compose + service configuration for full stack
│   ├── .env
│   ├── .env.example
│   ├── .gitignore
│   ├── docker-compose.yml
│   ├── minirag.service
│   ├── README.md
│   ├── env/
│   ├── minirag/
│   ├── nginx/
│   └── prometheus/
├── scripts/              
└── src/                         # application source
	├── __init__.py
	├── controllers/             # business logic controllers
	│   ├── BaseController.py
	│   ├── DataController.py
	│   ├── NLPController.py
	│   ├── ProcesController.py
	│   └── ProjectController.py
	├── helpers/
	├── models/                  # ORM & Pydantic models
	│   ├── AssetModel.py
	│   ├── BaseDataModel.py
	│   ├── ChunkModel.py
	│   ├── ProjectModel.py
	│   ├── db_schemes/
	│   └── enums/
	├── routes/                  # FastAPI routers and schemas
	│   ├── base.py
	│   ├── data.py               # upload & process endpoints
	│   ├── nlp.py
	│   └── schemas/
	├── stores/                  # LLM & VectorDB provider factories/adapters
	│   ├── llm/
	│   └── vectordb/
	├── utils/
	│   └── metrics.py            # prometheus integration
	└── views/
		└── index.html
```

Short notes:
- `src/routes/data.py` exposes the main ingestion endpoints: `/api/v1/data/upload/{project_id}` and `/api/v1/data/process/{project_id}`.
- `docker/docker-compose.yml` provides a full stack including FastAPI, pgvector (Postgres), Qdrant, Prometheus, and Grafana for local testing.
- `assets/` contains sample files and a local Qdrant DB export used by the Docker setup.

This structure intentionally separates routing, domain logic, and storage adapters so you can swap providers or extend behaviors with minimal friction.

## Installation ⚙️

Choose one of the following methods: local Python install or Docker Compose.

Prereqs
- Python 3.8+
- pip
- Docker & Docker Compose (if using the container option)

1) Install locally (virtualenv recommended)

```bash
# create and activate a virtualenv (optional but recommended)
python -m venv .venv
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt

# install editable package (optional)
pip install -e .
```

2) Run with Docker Compose (recommended for a complete stack)

```bash
# from repository root
cd docker
docker compose up --build -d
```

This will start the FastAPI app, a Postgres (pgvector) instance, Qdrant, Prometheus, Grafana and exporters as defined in `docker/docker-compose.yml`.

## Configuration 🧰

Settings are loaded from environment variables and the project's config helpers (`src/helpers/config.py`). Example important variables (found in project code and docker/env files):

- POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_MAIN_DATABASE
- VECTOR_DB_BACKEND (e.g. `qdrant` or `pgvector`)
- GENERATION_BACKEND (LLM provider key)
- EMBEDDING_BACKEND (embedding provider key)
- GENERATION_MODEL_ID, EMBEDDING_MODEL_ID, EMBEDDING_MODEL_SIZE
- PRIMARY_LANGUAGE, DEFAULT_LANGUAGE
- FILE_DEFAULT_CHUNK_SIZE

Docker Compose uses env files under `docker/env/` (for Postgres, Grafana, and the FastAPI app). Copy `.env.example` to `.env` and edit or place needed values into `docker/env/.env.app` before starting the stack if you need custom credentials.

## Usage 

Start locally (uvicorn):

```bash
# from repository root
uvicorn main:app --reload
```

Or start the full stack with Docker Compose (see Installation).

When running, the API serves at `http://localhost:8000` by default. The project also exposes metrics and monitoring endpoints when running with docker-compose.

### Key API endpoints (examples)

1) Upload a file

- POST /api/v1/data/upload/{project_id}
- Form payload: `file` (multipart file upload)

Example curl (upload):

```bash
curl -X POST "http://localhost:8000/api/v1/data/upload/1" \
	-F "file=@/path/to/document.pdf"
```

Successful response contains a JSON payload with a `file_id` (asset id/name) and a Signal field.

2) Process files (chunking & index to vector DB)

- POST /api/v1/data/process/{project_id}
- JSON body matches `ProcessRequest` schema:

```json
{
	"file_id": "<optional-file-name-or-id>",
	"chunk_size": 100,
	"overlap_size": 20,
	"do_reset": 0
}
```

Example curl (process):

```bash
curl -X POST "http://localhost:8000/api/v1/data/process/1" \
	-H "Content-Type: application/json" \
	-d '{"chunk_size":200, "overlap_size":40, "do_reset":1}'
```

Notes
- `do_reset=1` will delete the target vector collection and clear stored chunks for the project before re-indexing.
- If `file_id` is omitted, the endpoint will attempt to process all files registered for the project.

### Other helpful scripts

- `scripts/run_app.sh` — simple helper that installs the package in editable mode and runs uvicorn (useful for dev)
- `scripts/docker.sh` — helpers for docker usage (see file for details)

## Acknowledgments 🙏

- Built with FastAPI, SQLAlchemy, and many open-source libs listed in `requirements.txt`
- Monitoring integration courtesy of Prometheus and Grafana
- Inspired by common RAG patterns and LangChain-style embeddings + vector stores
 - Abubakr Soliman — excellent tutorials and walkthroughs — [YouTube playlist](https://www.youtube.com/playlist?list=PLvLvlVqNQGHCUR2p0b8a0QpVjDUg50wQj)


---
