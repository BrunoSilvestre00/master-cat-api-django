from plumber.base import BaseClient
from typing_extensions import Tuple


class Endpoints(object):
    HEALTH_CHECK = '/hc'


class PlumberClient(object):

    def __init__(self):
        self.base = BaseClient()

    def health_check(self) -> Tuple[bool, dict]:
        try:
            response = self.base.make_request(Endpoints.HEALTH_CHECK)
            response.raise_for_status()
            return True, response.json()
        except:
            return False, { 'status': 'Unhealthy!' }
