import threading
import secrets
import string
import requests
from requests.models import HTTPError


class ContiniousLoop():
    def __init__(self, crawl_threads, analyse_threads, analyse_url, crawler_url, analyse_APIKEY, crawler_APIKEY):
        self.active = False

        self.crawler_url = crawler_url
        self.analyse_url = analyse_url

        self.crawler_APIKEY = crawler_APIKEY
        self.analyse_APIKEY = analyse_APIKEY

        self.crawl_threads = crawl_threads
        self.analyse_threads = analyse_threads

        self.crawler_running_jobs = []
        self.analyse_running_jobs = []

        self.awaiting_contents = []


    def continious_loop(self):
        while self.active:
            if len(self.crawler_running_jobs) < crawl_threads:
                link = self.get_crawl_link()
                content = self.start_crawljob(link)
                self.awaiting_contents.append(content)

            if len(self.analyse_running_jobs) < analyse_threads and awaiting_contents:
                content = self.awaiting_contents.pop(0)
                results = self.start_analysejob(content)


    def get_crawl_link(self):
        pass

    def start_crawljob(self, link):
        pass


    def start_analysejob(self, content):
        job_id = generate_jobId()

        payload = {content}
        header = { "Authorization": f"Bearer {self.analyse_APIKEY}" }

        response = request.post(self.analyse_url, json=payload, header=header)

        if response == 200:
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




if __name__ == "__main__":

    crawler_url = ""
    analyse_url = ""
    crawler_APIKEY = ""
    analyse_APIKEY = ""
    crawl_threads = 1
    analyse_threads = 1


    loop = ContiniousLoop(
            crawler_url,
            analyse_url,
            crawler_APIKEY,
            analyse_APIKEY,
            crawl_threads,
            analyse_threads
            )
    print(loop.generate_jobId())

