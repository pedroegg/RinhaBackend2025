# ------ loading environment ------
from dotenv import load_dotenv
import sys
import os

if os.getenv('ENV') == 'development':
	load_dotenv('.env')
	# do something if needed

else:
	load_dotenv('prod.env', override=True)
# ------------------------------

# -------- init project --------
import logging
logging.basicConfig(level=int(os.getenv('LOG_LEVEL')), force=True)
logger = logging.getLogger("Main")

logger.info('intializing...')

from flask import Flask
from api.router import api as API

app = Flask(__name__)
app.register_blueprint(API)
app.templates_auto_reload = True

logger.info('init completed!')
# ------------------------------

# add and configure redis on the environment
# implement redis library for queue (LIST, LPUSH, BRPOP) and for caching (GET, SET, INCR, EXPIRE)
# implement flask-smorest + marshmallow
# implement service to use repository inserting (queue) and get data into/from redis
# implement repository to use redis
# implement model for responses and payloads

# adjust/configure uWSGI
# use redis as a queue integrated with the both app instances (read-only) to handle instabilities and avoiding inconsistency
# insert into redis the payments to be processed and let one or more consumers handle them (with tenacity retrying + using the fallback payment processor)
# save/update on redis after each payment processing, then the summary will always be correct for both app1 and app2 APIs


# another option would be to use the app1 and app2 to handle the payment processing with yours workers
# since we can configure uWSGI to have a lot of workers, maybe we can process a lot of requests simultaneously
# but then I will need to worry about bottlenecks, because if the payments processors become unavailable for so long I'm going to have problems
# and also, have a lot of workers running is very heavy