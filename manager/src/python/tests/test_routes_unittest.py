# manager/src/python/tests/test_routes_unittest.py
"""
Unittest-style tests for manager routes.
Run with:
  PYTHONPATH=manager/src/python python -m unittest discover -s manager/src/python/tests -v
This file similarly patches continous_loop before importing main so startup is inert.
"""
import os
import sys
import datetime
import unittest
from unittest.mock import MagicMock

TEST_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if TEST_ROOT not in sys.path:
    sys.path.insert(0, TEST_ROOT)

# patch continous_loop before importing the app
try:
    import continous_loop
    if hasattr(continous_loop, "loop") and hasattr(continous_loop.loop, "continious_loop"):
        continous_loop.loop.continious_loop = lambda *a, **k: None
except Exception:
    pass

from fastapi.testclient import TestClient
from main import app
from api.db.database import get_db

client = TestClient(app)


def _make_chainable_query(mock_query: MagicMock):
    for name in ("join", "filter", "order_by", "distinct", "options", "limit"):
        getattr(mock_query, name).return_value = mock_query
    return mock_query


class TestManagerRoutes(unittest.TestCase):
    def tearDown(self) -> None:
        app.dependency_overrides = {}
        
    def test_crawl_results_sets_analysed_on(self):
        mock_link = MagicMock()
        mock_session = MagicMock()
        mock_query = MagicMock()
        mock_query = _make_chainable_query(mock_query)
        mock_query.first.return_value = mock_link
        mock_session.query.return_value = mock_query

        import continous_loop
        continous_loop.loop.crawler_running_jobs = {"j1": "http://a"}

        app.dependency_overrides[get_db] = lambda: mock_session

        resp = client.post("/crawl-results", json={"job_id": "j1", "content": "x", "url": "http://a"},
                           headers={"Content-Type": "application/json"})
        if resp.status_code != 200:
            print("DEBUG /crawl-results resp.json():", resp.json())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(mock_link.analysed_on, datetime.date.today())
        mock_session.commit.assert_called()


if __name__ == "__main__":
    unittest.main()