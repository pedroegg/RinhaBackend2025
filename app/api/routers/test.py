import logging
logger = logging.getLogger("Test router")

from library.flask_utils import APIBlueprint

from api.handlers import test as handler
from api.schemas.test import TestQuery, TestInput

def new() -> APIBlueprint:
	api = APIBlueprint(name='test', import_name=__name__, logger=logger)

	@api.get('/test')
	@api.query(TestQuery)
	@api.response(200)
	def test_request(data: TestInput):
		return handler.test(data)

	return api
