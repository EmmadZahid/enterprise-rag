from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from enterprise_rag.app import create_app

DUMMY_ID = "00000000-0000-0000-0000-000000000001"
BASE = "/api/v1/documents"


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())


def test_health(client: TestClient) -> None:
    assert client.get("/health").json() == {"status": "ok"}


def test_list(client: TestClient) -> None:
    body = client.get(BASE).json()
    assert body["total"] == 1 and len(body["items"]) == 1


def test_get_found_and_missing(client: TestClient) -> None:
    assert client.get(f"{BASE}/{DUMMY_ID}").status_code == 200
    assert client.get(f"{BASE}/{uuid4()}").status_code == 404


def test_get_invalid_id(client: TestClient) -> None:
    assert client.get(f"{BASE}/not-a-uuid").status_code == 422


def test_create(client: TestClient) -> None:
    res = client.post(BASE, json={"title": "t", "content": "c"})
    assert res.status_code == 201
    assert res.json()["title"] == "t"


def test_create_validation(client: TestClient) -> None:
    assert client.post(BASE, json={"title": "", "content": "c"}).status_code == 422


def test_delete(client: TestClient) -> None:
    assert client.delete(f"{BASE}/{DUMMY_ID}").status_code == 204
    assert client.delete(f"{BASE}/{uuid4()}").status_code == 404
