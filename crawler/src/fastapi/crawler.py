import requests
import socket
from stem import Signal
from stem.control import Controller

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

    def crawl(self, urls: list):
        results = {}
        for url in urls:
            try:
                response = self.session.get(url)
                results[url] = {
                    "status_code": response.status_code,
                    "content": response.text
                }
            except requests.RequestException as e:
                results[url] = {"error": str(e)}
        return results