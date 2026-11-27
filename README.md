# TrackFlow — Job Application Tracker API

A lightweight, containerized RESTful backend built with **FastAPI**, **Pydantic**, and **SQLite** for tracking job applications, filtering by status or company, and viewing application pipeline statistics.

## Tech Stack
- **Backend:** Python 3.11+, FastAPI, Uvicorn
- **Validation:** Pydantic v2
- **Database:** SQLite (`sqlite3`)
- **Testing:** Pytest + FastAPI TestClient (`httpx`)
- **Containerization:** Docker

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Service health check |
| `POST` | `/applications` | Create a new job application |
| `GET` | `/applications` | List applications (supports `status`, `company`, `limit`, `offset`) |
| `GET` | `/applications/{id}` | Retrieve a single application by ID |
| `PATCH` | `/applications/{id}` | Partially update application details or status |
| `DELETE` | `/applications/{id}` | Delete an application |
| `GET` | `/stats` | Aggregated count of applications grouped by status |

## Run Locally

```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```

Open interactive Swagger UI at `http://127.0.0.1:8000/docs`.

## Run Tests

```bash
pytest -v
```

## Run with Docker

```bash
docker build -t trackflow-api .
docker run -p 8000:8000 trackflow-api
```
