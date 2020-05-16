import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


class Client:
    @staticmethod
    def get_session():
        s = requests.Session()
        retries = Retry(total=5000,
                        backoff_factor=0.1,
                        status_forcelist=[404])
        s.mount('http://', HTTPAdapter(max_retries=retries))
        return s
