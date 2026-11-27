from fastapi.testclient import TestClient
import database
from main import app

client = TestClient(app)


def test_crud_flow(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")
    database.init_db()

    # Create
    res = client.post(
        "/applications",
        json={"company": "Qualcomm", "role": "Python Engineer", "status": "Applied"},
    )
    assert res.status_code == 201
    app_id = res.json()["id"]

    # List & Filter
    list_res = client.get("/applications?status=Applied&company=qual")
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1

    # Update
    patch_res = client.patch(f"/applications/{app_id}", json={"status": "Interviewing"})
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "Interviewing"

    # Stats
    stats_res = client.get("/stats")
    assert stats_res.status_code == 200
    assert stats_res.json()["total_applications"] == 1

    # Delete & Verify 404
    del_res = client.delete(f"/applications/{app_id}")
    assert del_res.status_code == 204
    assert client.get(f"/applications/{app_id}").status_code == 404