import requests
from decouple import config as env

_PLUMBER_URL = env('PLUMBER_API_URL')

class Endpoints(object):
    HEALTH_CHECK = '/hc'

class PlumberClient(object):

    def __init__(self):
        self.url = _PLUMBER_URL

    def health_check(self) -> tuple:
        try:
            response = requests.get(f"{self.url}{Endpoints.HEALTH_CHECK}")
            response.raise_for_status()
            return True, response.json()
        except requests.exceptions.RequestException:
            return False, { 'status': 'Unhealthy!' }