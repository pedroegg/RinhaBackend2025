import logging
logger = logging.getLogger('Test handler')

import requests

from api.schemas.test import TestInput
from library.errors import InternalError, BadRequest, UnprocessableEntity

def test(data: TestInput) -> None:
	requests.get(f'https://httpbin.org/delay/{data["delay"]}')
