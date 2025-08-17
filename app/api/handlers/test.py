import logging
logger = logging.getLogger('Test handler')

import requests

from api.schemas.test import TestInput
from library.errors import InternalError, BadRequest, UnprocessableEntity

class TestHandler:
	def test(self, data: TestInput) -> None:
		requests.get(f'https://httpbin.org/delay/{data["delay"]}')
