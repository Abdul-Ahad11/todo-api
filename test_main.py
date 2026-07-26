import copy

import pytest
from fastapi.testclient import TestClient

import main

client = TestClient(main.app, raise_server_exceptions=False)


@pytest.fixture(autouse=True)
def reset_tasks():
    original = copy.deepcopy(main.tasks)
    yield
    main.tasks[:] = original


def test_missing_task_returns_structured_404():
    response = client.get('/tasks/999')
    assert response.status_code == 404
    assert response.json() == {
        "error": {"status": 404, "detail": "task 999 not found"}
    }


def test_invalid_body_returns_structured_422():
    response = client.post('/tasks', json={"title": ""})
    body = response.json()
    assert response.status_code == 422
    assert body["error"]["status"] == 422
    assert body["error"]["errors"][0]["loc"] == ["body", "title"]


def test_invalid_path_param_returns_structured_422():
    response = client.get('/tasks/abc')
    assert response.status_code == 422
    assert response.json()["error"]["detail"] == "request validation failed"


def test_unhandled_error_returns_structured_500():
    @main.app.get('/boom')
    def boom():
        raise ValueError("kaboom")

    try:
        response = client.get('/boom')
        assert response.status_code == 500
        assert response.json() == {
            "error": {"status": 500, "detail": "internal server error"}
        }
    finally:
        main.app.router.routes = [
            r for r in main.app.router.routes if getattr(r, "path", None) != '/boom'
        ]


def test_search_and_filter_combine():
    response = client.get('/tasks', params={"done": True, "search": "git"})
    assert response.status_code == 200
    assert [t["id"] for t in response.json()] == [3]


def test_search_only_matches_title():
    response = client.get('/tasks', params={"search": "internship"})
    assert [t["id"] for t in response.json()] == [2]


def test_ids_stay_unique_after_delete():
    assert client.delete('/tasks/3').status_code == 204
    created = client.post('/tasks', json={"title": "new"}).json()
    assert created["id"] not in (1, 2)
    assert len({t["id"] for t in main.tasks}) == len(main.tasks)


def test_update_missing_task_returns_404():
    response = client.put('/tasks/999', json={"title": "x", "done": True})
    assert response.status_code == 404


def test_delete_missing_task_returns_404():
    response = client.delete('/tasks/999')
    assert response.status_code == 404
