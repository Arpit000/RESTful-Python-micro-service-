from fastapi.testclient import TestClient

from app.main import app, _tasks

client = TestClient(app)


def setup_function() -> None:
    _tasks.clear()


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_task_crud_lifecycle() -> None:
    created = client.post(
        "/api/v1/tasks",
        json={"title": "Write tests", "description": "Cover the API"},
    )
    assert created.status_code == 201
    task = created.json()
    task_id = task["id"]
    assert task["completed"] is False

    listed = client.get("/api/v1/tasks")
    assert listed.status_code == 200
    assert [item["id"] for item in listed.json()] == [task_id]

    fetched = client.get(f"/api/v1/tasks/{task_id}")
    assert fetched.status_code == 200
    assert fetched.json()["title"] == "Write tests"

    updated = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"completed": True},
    )
    assert updated.status_code == 200
    assert updated.json()["completed"] is True
    assert updated.json()["title"] == "Write tests"

    deleted = client.delete(f"/api/v1/tasks/{task_id}")
    assert deleted.status_code == 204
    assert client.get(f"/api/v1/tasks/{task_id}").status_code == 404


def test_create_task_validates_title() -> None:
    response = client.post("/api/v1/tasks", json={"title": ""})

    assert response.status_code == 422


def test_unknown_task_returns_not_found() -> None:
    response = client.get("/api/v1/tasks/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
