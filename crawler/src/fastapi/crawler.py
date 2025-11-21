import requests
import socket
from stem import Signal
from stem.control import Controller

class Crawler:
    def __init__(self):
        tor_ip = socket.gethostbyname('tor')
        print("Resolved tor container IP:", tor_ip)
        self.controller = Controller.from_port(address=tor_ip, port=9051)
        self.controller.authenticate()
        self.controller.signal(Signal.NEWNYM)

        self.session = requests.Session()
        self.session.proxies = {
            'http': 'socks5h://tor:9050',
            'https': 'socks5h://tor:9050'
        }

    def crawl(self, urls: list):
        results = {}
        for url in urls:
            try:
                response = self.session.get(url, timeout=10)
                results[url] = {
                    "status_code": response.status_code,
                    "content": response.text[:200]  # Store only first 200 chars
                }
            except requests.RequestException as e:
                results[url] = {"error": str(e)}
        return results