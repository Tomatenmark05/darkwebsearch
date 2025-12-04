from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_crawl_and_single_status_endpoint():
    crawl_data = {"addresses": "https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/"}
    response = client.post("/crawl", json=crawl_data)
    assert "job_id" in response.json()
    job_id = response.json()["job_id"]

    status_response = client.get(f"/status/{job_id}")
    assert status_response.json()["job_id"] == job_id
    assert "status" in status_response.json()
    assert "created_at" in status_response.json()
    assert "finished_at" in status_response.json()
    assert "analysis_status" in status_response.json()

def test_all_status_endpoint():
    response = client.get("/status")
    assert isinstance(response.json(), list)
    assert len(response.json()) != 0
