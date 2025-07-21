import logging
logger = logging.getLogger('Handler')

from decimal import Decimal

from api.entities.payment import PaymentSummaryEntity, PaymentSummaryItem
from api.schemas.payment import ProcessPaymentInput, PaymentSummaryInput
from library.errors import InternalError, BadRequest, UnprocessableEntity

def process_payment(data: ProcessPaymentInput) -> None:
	# insert payment into redis queue

	return None

def payments_summary(data: PaymentSummaryInput) -> PaymentSummaryEntity:
	summary = PaymentSummaryEntity(
		default=PaymentSummaryItem(43236, Decimal(415542345.98)),
		fallback=PaymentSummaryItem(423545, Decimal(329347.34)),
	)

	return summary
