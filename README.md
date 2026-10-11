# Python RESTful Microservice

A small REST API built with FastAPI. The starter manages tasks using in-memory storage, so data resets when the service restarts.

## Requirements

- Python 3.10 or newer

## Setup

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

## Run

```sh
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive API documentation is at `/docs`; the health check is `/health`.

## Endpoints

- `GET /health` checks service health.
- `POST /api/v1/tasks` creates a task (`title`, optional `description`).
- `GET /api/v1/tasks` lists tasks.
- `GET /api/v1/tasks/{task_id}` gets one task.
- `PATCH /api/v1/tasks/{task_id}` updates supplied fields (`title`, `description`, `completed`).
- `DELETE /api/v1/tasks/{task_id}` deletes a task.

## Test

```sh
pytest
```

## Run with Docker

Build an image from the project directory:

```sh
docker build -t tasks-api:dev .
```

Start a container and forward port 8000 on your computer to port 8000 in the container:

```sh
docker run --rm --name tasks-api -p 8000:8000 tasks-api:dev
```

Open `http://127.0.0.1:8000/docs` to try the API. Stop the container with `Ctrl+C`. The `--rm` option removes the stopped container; the built image remains available. Task data is still in memory and is lost when the container stops.

## Next step

Replace the in-memory dictionary in `app/main.py` with a persistent repository when you are ready to add a database.
