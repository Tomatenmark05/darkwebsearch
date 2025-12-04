import requests
import socket
import uuid
import threading
from typing import Dict, List, Optional
import time
from stem import Signal
from stem.control import Controller
import json

JOB_STORE: Dict[str, Dict] = {}

class Crawler:
    def __init__(self):
        tor_ip = socket.gethostbyname('tor') # Because stem doesn't resolve docker service names and checks for valid IP format
        self.controller = Controller.from_port(address=tor_ip, port=9051)
        self.controller.authenticate()
        self.controller.signal(Signal.NEWNYM)

        self.session = requests.Session()
        self.session.proxies = {
            'http': 'socks5h://tor:9050',
            'https': 'socks5h://tor:9050'
        }

    def _perform_crawl(self, job_id: str, urls: List[str]):
        print("Crawling url: ", urls)
        JOB_STORE[job_id]['status'] = 'running'
        results: Dict[str, str] = {}

        for url in urls:
            try:
                response = self.session.get(url, timeout=30)
                results[url] = response.text
            except requests.RequestException as e:
                results[url] = {"error": str(e)}

        JOB_STORE[job_id]['status'] = 'finished'
        JOB_STORE[job_id]['finished_at'] = time.time()
        JOB_STORE[job_id]['results'] = results

        print(results)

        try:
            print("Send results to Manager")

            headers = { "Authorization": f"Bearer changeme" }
            # `results` is a dict mapping url -> response (or error). The manager expects
            # `content` to be a string, so send the crawled HTML/text for the URL we posted
            # in `url` (urls[0]). If the crawl produced an error dict, stringify it.
            for key, value in results.items():
                resp = requests.post("http://manager:8000/crawl-results", json={
                    'url': key,
                    'job_id': job_id,
                    'content': value,
                }, headers=headers, timeout=10)
            
            JOB_STORE[job_id]["analysis_status"] = 'sent off'
        except Exception as exc:
            print(exc)
            pass


    def start_crawl(self, urls: List[str]) -> str:
        job_id = str(uuid.uuid4())

        JOB_STORE[job_id] = {
            'status': 'queued',
            'created_at': time.time(),
            'urls': list(urls),
            'results': None,
        }

        # Start background thread to perform the crawl (requests is blocking)
        thread = threading.Thread(target=self._perform_crawl, args=(job_id, urls), daemon=True)
        thread.start()

        return job_id

    @staticmethod
    def get_job(job_id: str) -> Optional[Dict]:
        return JOB_STORE.get(job_id)
    
    @staticmethod
    def get_jobs() -> Dict:
        return JOB_STORE
