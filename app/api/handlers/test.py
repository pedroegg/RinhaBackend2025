import logging
logger = logging.getLogger('Handler')

import requests

from api.schemas.test import TestInput
from library.errors import InternalError, BadRequest, UnprocessableEntity

def test(data: TestInput) -> None:
	requests.get(f'https://httpbin.org/delay/{data["delay"]}')
