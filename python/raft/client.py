import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


class Client:
    def __init__(self):
        self.session = None

    def __enter__(self):
        self.session = requests.Session()
        retries = Retry(total=5000,
                        backoff_factor=0.1,
                        status_forcelist=[404])
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.session = None
