from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_crawl_endpoint():
    response = client.post("/crawler", '{"addresses": "https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/"}')
    assert "job_id" in response

def test_single_status_endpoint():
    pass

def test_all_status_endpoint():
    pass
