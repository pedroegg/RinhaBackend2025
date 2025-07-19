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

# add redis to docker-compose
# configure redis
# implement redis library
# implement flask-smorest + marshmallow
# implement service
# implement repository
# implement model