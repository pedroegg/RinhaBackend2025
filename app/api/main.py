from dotenv import load_dotenv
import os

if os.getenv('ENV') == 'development':
	load_dotenv('.env')
	# do something if needed
else:
	load_dotenv('prod.env', override=True)

import logging
logging.basicConfig(level=int(os.getenv('LOG_LEVEL')), force=True)
logger = logging.getLogger('API')

from flask import Flask
from flask.json.provider import DefaultJSONProvider
from flask_smorest import Api
import simplejson as sj
from typing import Any

class SimpleJSONProvider(DefaultJSONProvider):
	def dumps(self, obj: Any, **kwargs: Any) -> str:
		kwargs.setdefault('use_decimal', True)
		return sj.dumps(obj, **kwargs)

	def loads(self, s: str | bytes, **kwargs: Any) -> Any:
		return sj.loads(s, **kwargs)

logger.info('intializing...')

app = Flask(__name__)
app.config['API_TITLE'] = os.getenv('API_TITLE')
app.config['API_VERSION'] = os.getenv('API_VERSION')
app.config['OPENAPI_VERSION'] = os.getenv('OPENAPI_VERSION')
app.config['OPENAPI_URL_PREFIX'] = os.getenv('OPENAPI_URL_PREFIX')
app.config['OPENAPI_SWAGGER_UI_PATH'] = os.getenv('OPENAPI_SWAGGER_UI_PATH')
app.config['OPENAPI_SWAGGER_UI_URL'] = os.getenv('OPENAPI_SWAGGER_UI_URL')

app.json = SimpleJSONProvider(app)
api = Api(app)

from api.routers import payment_api, test_api

for bp in (payment_api, test_api):
	api.register_blueprint(bp)
	logger.info(f'{bp.name} API loaded!')

logger.info('ready!')

# implement redis library for queue (LIST, LPUSH, BRPOP or Streams + Consumer Groups) and for caching (GET, SET, INCR, EXPIRE)
# implement service to use repository inserting (queue) and get data into/from redis
# implement repository to use redis
# implement grafana + prometheus for monitoring
# check why all the schemas aren't appearing on the generated doc

# use redis as a queue integrated with the both app instances (read-only) to handle instabilities and avoiding inconsistency
# insert into redis the payments to be processed and let one or more consumers handle them (with tenacity retrying + using the fallback payment processor)
# save/update on redis after each payment processing, then the summary will always be correct for both app1 and app2 APIs

# multiple instances of the consumer application, each one consuming and processing one batch per time with async or threads
# or
# one consumer application that runs 4 async workers on separated threads, each one worker consuming one message or a batch of messages