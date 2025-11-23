import threading
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


    def continious_loop(self):
        while self.active:
            print("Loop start")
            if len(self.crawler_running_jobs) < self.crawl_thread:
                link = self.get_crawl_link()
                content = self.start_crawljob(link)
                self.awaiting_contents.append(content)

            if len(self.analyse_running_jobs) < self.analyse_threads and self.awaiting_contents:
                content = self.awaiting_contents.pop(0)
                results = self.start_analysejob(content)


    def get_crawl_link(self):
        return "https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/"

    def start_crawljob(self, link):
        job_id = self.generate_jobId

        link = self.get_crawl_link()

        payload = {"addresses": link}
        #header = { "Authorization": f"Bearer {self.crawler_APIKEY}" }

        response = requests.post(self.crawler_url, json=payload)

        if response.status_code == 200:
            self.crawler_running_jobs.append(job_id)
            return response.content
        else:
            raise Exception("Error: Crawler Job could not be started")


    def start_analysejob(self, content):
        job_id = self.generate_jobId()

        payload = {content}
        header = { "Authorization": f"Bearer {self.analyse_APIKEY}" }

        response = requests.post(self.analyse_url, json=payload, headers=header)

        if response.status_code == 200:
            self.analyse_running_jobs.append(job_id)
            return True
        else:
            raise Exception("Error: Analyse Job could not be started")

    @staticmethod
    def generate_jobId():
        length = 12
        alphabet = string.ascii_letters + string.digits

        job_id = ''.join(secrets.choice(alphabet) for _ in range(length))

        return job_id


crawler_url = "http://crawler:8080/crawl"
analyse_url = "http://analyze:8080/analys"
crawler_APIKEY = ""
analyse_APIKEY = ""
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


