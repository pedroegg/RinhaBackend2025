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
from decimal import Decimal
from typing import List, Tuple, Dict

from domain.repository.payment import PaymentRepository

repo = PaymentRepository()

stop_event = asyncio.Event()
def _graceful_shutdown():
	logger.info('signal received, shutting down...')
	stop_event.set()

logger.info('init completed!')
# ---------------------------------

async def worker(consumer_name: str):
	while not stop_event.is_set():
		try:
			messages: List[Tuple[str, Dict[str, str]]] = repo.read_payments(
				consumer_name=consumer_name,
				count=16,
				block_ms=5000,
			)
		
		except Exception as e:
			logger.exception('failed to read from redis stream')
			await asyncio.sleep(1)
			continue

		if not messages:
			continue

		for message_id, data in messages:
			try:
				amount = Decimal(str(data.get('amount', '0')))
				
				# process the payment here (call external processor, etc.)
				# on success:
				
				repo.increment_processed(amount=amount)
				repo.ack_payment(message_id)
			
			except Exception:
				logger.exception(f'failed to process message {message_id}')
				continue

async def main():
	loop = asyncio.get_running_loop()
	for sig in (signal.SIGINT, signal.SIGTERM):
		loop.add_signal_handler(sig, _graceful_shutdown)

	await worker()

if __name__ == '__main__':
	asyncio.run(main())
