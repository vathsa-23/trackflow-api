from fastapi import FastAPI, HTTPException, Query
from database import get_connection, init_db
from schemas import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationStatus,
    ApplicationUpdate,
)

app = FastAPI(
    title="TrackFlow — Job Application Tracker API",
    description="RESTful backend API for tracking job applications with filtering, analytics, and SQLite persistence.",
    version="1.0.0",
)

init_db()


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "trackflow-api"}


@app.post("/applications", response_model=ApplicationResponse, status_code=201)
def create_application(payload: ApplicationCreate):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO applications (company, role, status, location, notes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (payload.company, payload.role, payload.status, payload.location, payload.notes),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM applications WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
    return dict(row)


@app.get("/applications", response_model=list[ApplicationResponse])
def list_applications(
    status: ApplicationStatus | None = None,
    company: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    query = "SELECT * FROM applications WHERE 1=1"
    params: list = []

    if status:
        query += " AND status = ?"
        params.append(status)
    if company:
        query += " AND LOWER(company) LIKE ?"
        params.append(f"%{company.lower()}%")

    query += " ORDER BY id DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
    return [dict(row) for row in rows]


@app.get("/applications/{app_id}", response_model=ApplicationResponse)
def get_application(app_id: int):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM applications WHERE id = ?", (app_id,)
        ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Application not found")
    return dict(row)


@app.patch("/applications/{app_id}", response_model=ApplicationResponse)
def update_application(app_id: int, payload: ApplicationUpdate):
    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    with get_connection() as conn:
        existing = conn.execute(
            "SELECT * FROM applications WHERE id = ?", (app_id,)
        ).fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="Application not found")

        set_clause = ", ".join(f"{col} = ?" for col in updates.keys())
        values = list(updates.values()) + [app_id]
        conn.execute(f"UPDATE applications SET {set_clause} WHERE id = ?", values)
        conn.commit()
        updated = conn.execute(
            "SELECT * FROM applications WHERE id = ?", (app_id,)
        ).fetchone()
    return dict(updated)


@app.delete("/applications/{app_id}", status_code=204)
def delete_application(app_id: int):
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM applications WHERE id = ?", (app_id,))
        conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Application not found")
    return None


@app.get("/stats")
def get_stats():
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
        rows = conn.execute(
            "SELECT status, COUNT(*) as count FROM applications GROUP BY status"
        ).fetchall()
    breakdown = {row["status"]: row["count"] for row in rows}
    return {"total_applications": total, "by_status": breakdown}