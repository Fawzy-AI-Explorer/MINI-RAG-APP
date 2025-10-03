#!/bin/bash
set -e

echo "Running database migrations..."

cd /app
alembic -c src/models/db_schemes/miniragdb/alembic.ini upgrade head

exec "$@"