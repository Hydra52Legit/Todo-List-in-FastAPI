# Todo-List-in-FastAPI
This repository contains a simple multiuser todo list API built with FastAPI,
SQLAlchemy and PostgreSQL (via Docker). For local development you can also
use SQLite by overriding the `DATABASE_URL` environment variable.

## Local setup

1. create and activate a virtual environment:
	```bash
	python -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt
	```
2. copy `.env` and adjust values if needed. By default `.env` points at a
	Postgres container (`postgresql://user:password@db:5432/todo`). If you are
	running the API locally without Docker you should either comment out that
	line and uncomment the SQLite URL below it, or export the variable manually:
	```bash
	export DATABASE_URL=sqlite:///./todo.db
	```
	(The startup handler will log a warning if the configured database is
	unreachable, but it won't crash the application.)

3. start the server:
	```bash
	uvicorn app.main:app --reload
	```

## Using Docker Compose

The included `app/docker-compose.yml` defines two services: `api` and `db`.
Be sure the Docker daemon is running, then execute:

```bash
docker compose -f app/docker-compose.yml up --build
```

The compose file mounts the repository root into the container so your
changes appear live in the service. The `api` service reads `DATABASE_URL`
from its environment (set to point at the `db` service).

A few more notes
- `requirements.txt` now contains `httpx` so that the FastAPI `TestClient`
  works in your tests.
- The SQLAlchemy models define `User`, `Project` and `Task` with proper
  relationships; table creation happens on startup to avoid import-time
  connection errors.

## Password length

- The underlying bcrypt algorithm limits passwords to 72 bytes. The
	application enforces this and will return a **400 Bad Request** if you
	attempt to register with a longer password. Pick a shorter string or
	truncate manually (e.g. `mypassword[:72]`).
