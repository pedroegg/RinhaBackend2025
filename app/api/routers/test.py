import logging
logger = logging.getLogger("Router")

from library.flask_utils import APIBlueprint
from library.errors import BaseError, InternalError, BadRequest

from api.handlers import test as handler
from api.schemas.test import TestQuery, TestInput

api = APIBlueprint(name='test', import_name=__name__, logger=logger)

@api.get('/test')
@api.query(TestQuery)
@api.response(200)
def test_request(data: TestInput):
	return handler.test(data)
