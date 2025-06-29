#!/bin/bash
echo "Waiting for Postgres to be ready..."
until pg_isready -h postgres -p 5432; do
  sleep 1
done

echo "Running migrations..."
alembic upgrade head

echo "Starting server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
