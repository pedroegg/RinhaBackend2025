# ------ loading environment ------
from dotenv import load_dotenv
import os

if os.getenv('ENV') == 'development':
	load_dotenv('.env')
	# do something if needed
else:
	load_dotenv('prod.env', override=True)
# ---------------------------------

# --------- init consumer ---------
import logging
logging.basicConfig(level=int(os.getenv('LOG_LEVEL')), force=True)
logger = logging.getLogger('Consumer')

# omitting libs DEBUG logs when in dev
logging.getLogger("asyncio").setLevel(logging.INFO)

logger.info('initializing...')

import asyncio
import signal

stop_event = asyncio.Event()

def _graceful_shutdown():
	logger.info('signal received, shutting down...')
	stop_event.set()

logger.info('init completed!')
# ---------------------------------

async def worker():
	while not stop_event.is_set():
		print(f'worker running on {asyncio.get_running_loop().time()}')

		try:
			msgs = []

		except Exception as e:
			logger.error('failed to consume from redis')
			continue

		for msg in msgs:
			a = 1

		await asyncio.sleep(10) #remove later

async def main():
	loop = asyncio.get_running_loop()
	for sig in (signal.SIGINT, signal.SIGTERM):
		loop.add_signal_handler(sig, _graceful_shutdown)

	await worker()

if __name__ == '__main__':
	asyncio.run(main())
