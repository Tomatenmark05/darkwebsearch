import os
import time
import unittest
from unittest.mock import patch, MagicMock

import crawler


class FakeResponse:
    def __init__(self, status_code=200, text='ok'):
        self.status_code = status_code
        self.text = text


class TestCrawler(unittest.TestCase):
    def setUp(self):
        # Patch Controller.from_port so we don't try to talk to a real Tor
        patcher = patch('crawler.Controller.from_port')
        self.addCleanup(patcher.stop)
        self.mock_from_port = patcher.start()

        fake_controller = MagicMock()
        fake_controller.authenticate.return_value = None
        fake_controller.signal.return_value = None
        self.mock_from_port.return_value = fake_controller

        # Patch DNS resolution for the 'tor' hostname so __init__ doesn't fail
        patcher_dns = patch('crawler.socket.gethostbyname', return_value='127.0.0.1')
        self.addCleanup(patcher_dns.stop)
        self.mock_gethost = patcher_dns.start()

    def wait_for_job_finished(self, crawler_instance, job_id, timeout=3.0):
        start = time.time()
        while time.time() - start < timeout:
            job = crawler_instance.get_job(job_id)
            if job and job.get('status') == 'finished':
                return job
            time.sleep(0.05)
        return None

    def test_start_crawl_and_get_job(self):
        # Patch the session.get method to return a predictable response
        with patch.object(crawler.requests.Session, 'get', return_value=FakeResponse(200, 'hello')) as mock_get:
            c = crawler.Crawler()
            job_id = c.start_crawl(['http://example.com'])

            # job should be in the instance JOB_STORE
            self.assertIn(job_id, c.JOB_STORE)

            job = self.wait_for_job_finished(c, job_id, timeout=5.0)
            self.assertIsNotNone(job, 'Job did not finish in time')
            self.assertEqual(job['status'], 'finished')
            self.assertIn('http://example.com', job['results'])
            # current implementation stores the response body as a string
            self.assertEqual(job['results']['http://example.com'], 'hello')

            # ensure we actually called requests.get
            mock_get.assert_called()

    def test_get_job_and_get_jobs(self):
        with patch.object(crawler.requests.Session, 'get', return_value=FakeResponse(200, 'ok')):
            c = crawler.Crawler()
            job_id = c.start_crawl(['http://a.example'])

            job = self.wait_for_job_finished(c, job_id, timeout=5.0)
            self.assertIsNotNone(job)

            # get_job should return the same object
            fetched = c.get_job(job_id)
            self.assertEqual(fetched, job)

            # get_jobs should return the internal store containing the job
            all_jobs = c.get_jobs()
            self.assertIn(job_id, all_jobs)

    def test_manager_post_attempted(self):
        # verify the crawler attempts to POST results to manager endpoint
        with patch.object(crawler.requests.Session, 'get', return_value=FakeResponse(200, 'payload')):
            with patch('crawler.requests.post') as mock_post:
                mock_post.return_value = MagicMock(status_code=200)

                c = crawler.Crawler()
                job_id = c.start_crawl(['http://example.org'])

                job = self.wait_for_job_finished(c, job_id, timeout=5.0)
                self.assertIsNotNone(job)

                # Verify POST was attempted to manager endpoint
                mock_post.assert_called()
   


if __name__ == '__main__':
    unittest.main()