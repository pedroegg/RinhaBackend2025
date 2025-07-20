# ------ loading environment ------
from dotenv import load_dotenv
import os

if os.getenv('ENV') == 'development':
	load_dotenv('.env')
	# do something if needed
else:
	load_dotenv('prod.env', override=True)
# ------------------------------

# ------ models download ------
import logging
logging.basicConfig(level=int(os.getenv('LOG_LEVEL')), force=True)
logger = logging.getLogger("Setup")

# do something if needed

logger.info('setup completed!')
# --------------------------