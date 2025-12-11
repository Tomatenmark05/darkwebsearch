# manager/src/python/tests/test_routes_pytest.py
"""
Pytest tests for manager FastAPI routes.
Run from repo root:
  PYTHONPATH=manager/src/python pytest manager/src/python/tests -q
This test file ensures continous_loop.loop.continious_loop is a no-op
so TestClient's startup doesn't run background behaviour during tests.
"""
import os
import sys
import datetime
from unittest.mock import MagicMock

# ensure the package root (manager/src/python) is on the path when tests are run from repo root
TEST_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if TEST_ROOT not in sys.path:
    sys.path.insert(0, TEST_ROOT)

# patch continous_loop before importing the app so startup won't run the real loop
try:
    import continous_loop
    # make the startup continuous loop a no-op for tests
    if hasattr(continous_loop, "loop") and hasattr(continous_loop.loop, "continious_loop"):
        continous_loop.loop.continious_loop = lambda *a, **k: None
except Exception:
    # If module not present or different shape, ignore — tests will still try to run
    pass

from fastapi.testclient import TestClient
from main import app  # now safe to import after patching
from api.db.database import get_db

client = TestClient(app)


def _make_chainable_query(mock_query: MagicMock):
    """Make common SQLAlchemy query methods return the same mock_query for chaining"""
    for name in ("join", "filter", "order_by", "distinct", "options", "limit"):
        getattr(mock_query, name).return_value = mock_query
    return mock_query


def teardown_function(_):
    # clear overrides after each test
    app.dependency_overrides = {}



def test_crawl_results_sets_analysed_on():
    mock_link = MagicMock()

    mock_session = MagicMock()
    mock_query = MagicMock()
    # make chainable first
    mock_query = _make_chainable_query(mock_query)
    # because filter() returns mock_query, ensure first() returns mock_link
    mock_query.first.return_value = mock_link

    mock_session.query.return_value = mock_query

    # ensure mapping job_id -> url exists as the route expects
    import continous_loop
    continous_loop.loop.crawler_running_jobs = {"job-123": "http://example.com"}

    app.dependency_overrides[get_db] = lambda: mock_session

    resp = client.post("/crawl-results", json={
        "job_id": "job-123",
        "content": "<html>ok</html>",
        "url": "http://example.com"
    }, headers={"Content-Type": "application/json"})
    if resp.status_code != 200:
        print("DEBUG /crawl-results resp.json():", resp.json())
    assert resp.status_code == 200

    # route assigns analysed_on = datetime.date.today()
    assert mock_link.analysed_on == datetime.date.today()
    mock_session.commit.assert_called()