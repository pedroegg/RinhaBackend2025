import os
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict

from domain.entities.payment import PaymentSummaryEntity, PaymentSummaryItem

from library.redis import RedisClient

PAYMENTS_STREAM = os.getenv('PAYMENTS_STREAM')
PAYMENTS_GROUP = os.getenv('PAYMENTS_GROUP')
PROCESSED_COUNTER_KEY = os.getenv('PROCESSED_COUNTER_KEY')
PROCESSED_AMOUNT_KEY = os.getenv('PROCESSED_AMOUNT_KEY')

class PaymentRepository:
	db: RedisClient

	def __init__(self, db: RedisClient) -> None:
		self.db = db

	def enqueue_payment(self, correlation_id: str, amount: Decimal) -> str:
		payload: Dict[str, Any] = {
			'correlation_id': correlation_id,
			'amount': str(amount),
		}
		
		return self.db.add_to_stream(stream=PAYMENTS_STREAM, fields=payload)

	def read_payments(self, consumer_name: str, count: int = 10, block_ms: int = 5000):
		return self.db.read_group(
			stream=PAYMENTS_STREAM,
			group=PAYMENTS_GROUP,
			consumer=consumer_name,
			count=count,
			block_ms=block_ms,
		)

	def ack_payment(self, message_id: str) -> int:
		return self.db.ack(stream=PAYMENTS_STREAM, group=PAYMENTS_GROUP, message_id=message_id)

	def increment_processed(self, amount: Decimal) -> None:
		self.db.incrby(PROCESSED_COUNTER_KEY, 1)
		
		cents = int((amount * 100).to_integral_value())
		self.db.incrby(PROCESSED_AMOUNT_KEY, cents)

	def get_summary(self, start: datetime, end: datetime) -> PaymentSummaryEntity:
		count_raw = self.db.get(PROCESSED_COUNTER_KEY)	
		amount_cents_raw = self.db.get(PROCESSED_AMOUNT_KEY)
		count = int(count_raw) if count_raw is not None else 0
		amount_cents = int(amount_cents_raw) if amount_cents_raw is not None else 0
		total_amount = Decimal(amount_cents) / Decimal(100)
		# For now, expose same numbers for default and fallback to satisfy schema
		item = PaymentSummaryItem(requests_number=count, total_amount=total_amount)
		return PaymentSummaryEntity(default=item, fallback=item)

