import threading
import time
import asyncio
import secrets
import string
import requests
from requests.models import HTTPError


class ContiniousLoop():
    def __init__(self, crawl_thread, analyse_thread, analyse_url, crawler_url, analyse_APIKEY, crawler_APIKEY):
        self.active = False

        self.crawler_url = crawler_url
        self.analyse_url = analyse_url

        self.crawler_APIKEY = crawler_APIKEY
        self.analyse_APIKEY = analyse_APIKEY

        self.crawl_thread: int = crawl_thread
        self.analyse_threads: int = analyse_thread

        self.crawler_running_jobs = []
        self.analyse_running_jobs = []

        self.awaiting_contents = []


    async def continious_loop(self):
        while self.active:
            print("Loop start")
            print(self.crawler_running_jobs)
            if len(self.crawler_running_jobs) < self.crawl_thread:
                link = self.get_crawl_link()
                content = self.start_crawljob(link)
                self.awaiting_contents.append(content)
            await asyncio.sleep(1)

    def get_crawl_link(self):
        return "https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/"

    def start_crawljob(self, link):
        # Use provided link; fall back to default if None/empty
        if not link:
            link = self.get_crawl_link()

        payload = {"addresses": link}
        # header = { "Authorization": f"Bearer {self.crawler_APIKEY}" }

        response = requests.post(self.crawler_url, json=payload)

        try:
            data = response.json()
        except ValueError:
            raise Exception(f"Error: Crawler returned non-JSON response (status {response.status_code}): {response.text}")

        job_id = data.get("job_id")
        if response.status_code == 200 and job_id:
            self.crawler_running_jobs.append(job_id)
            # return parsed JSON so downstream code gets a serializable object
            return data
        else:
            raise Exception(f"Error: Crawler Job could not be started (status {response.status_code}): {response.text}")


    def start_analysejob(self, content):

        payload = {"content": content}

        headers = { "Authorization": f"Bearer {self.analyse_APIKEY}" }

        response = requests.post(self.analyse_url, json=payload, headers=headers)

        try:
            data = response.json()
        except ValueError:
            raise Exception(f"Error: Analyse returned non-JSON response (status {response.status_code}): {response.text}")

        job_id = data.get("jobId")

        if response.status_code == 202 and job_id:
            self.analyse_running_jobs.append(job_id)
            return True
        else:
            raise Exception(f"Error: Analyse Job could not be started (status {response.status_code}): {response.text}")

    @staticmethod
    def generate_jobId():
        length = 12
        alphabet = string.ascii_letters + string.digits

        job_id = ''.join(secrets.choice(alphabet) for _ in range(length))

        return job_id


crawler_url = "http://crawler:8080/crawl"
analyse_url = "http://analyzer:8000/analyze"
crawler_APIKEY = ""
analyse_APIKEY = "this-is-my-super-secure-api-key"
crawl_thread = 1
analyse_thread = 1


loop = ContiniousLoop(
    crawler_url = crawler_url,
    analyse_url = analyse_url,
    crawler_APIKEY = crawler_APIKEY,
    analyse_APIKEY = analyse_APIKEY,
    crawl_thread = crawl_thread,
    analyse_thread = analyse_thread
    )


