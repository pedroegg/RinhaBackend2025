import logging
logger = logging.getLogger('Payment handler')

from decimal import Decimal

from domain.service.payment import PaymentService

from api.schemas.payment import (
	ProcessPaymentInput,
	PaymentSummaryInput, PaymentSummaryOutput
)

from library.errors import InternalError, BadRequest, UnprocessableEntity

class PaymentHandler:
	service: PaymentService

	def __init__(self, service: PaymentService) -> None:
		self.service = service

	def process_payment(self, data: ProcessPaymentInput) -> None:
		self.service.process_payment(
			correlation_id=str(data['correlation_id']),
			amount=Decimal(data['amount']),
		)
		
		return None

	def payments_summary(self, data: PaymentSummaryInput) -> PaymentSummaryOutput:
		#ver se converte o entity pro output msm ou se precisa fazer na mão
		return self.service.get_summary(data['start'], data['end'])
