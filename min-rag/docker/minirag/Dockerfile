FROM ghcr.io/astral-sh/uv:0.6.14-python3.10-bookworm

WORKDIR /app

# Install additional system dependencies for lxml and other packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libavif-dev pkg-config \
    libjpeg-dev \
    gcc unzip zip \
    python3-dev \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
COPY pyproject.toml /app/pyproject.toml

# RUN uv pip install -r app/requirements.txt --system
RUN uv pip install -r requirements.txt --system


COPY .vscode/ /app/.vscode/
COPY assets/ /app/assets/
COPY config/ /app/config/
# COPY docker/ /app/docker/
COPY scripts/ /app/scripts/
COPY src/ /app/src/
COPY .env /app/.env
COPY .env.example /app/.env.example
COPY .gitignore /app/.gitignore
COPY main.py /app/main.py
COPY README.md /app/README.md
COPY requirements.txt /app/requirements.txt


# Create directory structure for Alembic
RUN mkdir -p /app/src/models/db_schemes/miniragdb/

COPY docker/minirag/alembic.ini /app/src/models/db_schemes/miniragdb/alembic.ini

COPY docker/minirag/entrypoint.sh /entrypoint.sh

RUN pip install -e .

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

