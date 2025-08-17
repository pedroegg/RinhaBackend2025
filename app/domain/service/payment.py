from datetime import datetime
from decimal import Decimal

from domain.repository.payment import PaymentRepository
from domain.entities.payment import PaymentSummaryEntity

class PaymentService:
	repo: PaymentRepository
	
	def __init__(self, repository: PaymentRepository) -> None:
		self.repo = repository

	def process_payment(self, correlation_id: str, amount: Decimal) -> None:
		self.repo.enqueue_payment(correlation_id, amount)
		return None

	def get_summary(self, start: datetime, end: datetime) -> PaymentSummaryEntity:
		return self.repo.get_summary(start, end)
