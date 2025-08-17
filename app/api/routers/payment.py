import logging
logger = logging.getLogger("Payment router")

from domain.service.payment import PaymentService
from library.flask_utils import APIBlueprint

from api.handlers.payment import PaymentHandler
from api.schemas.payment import (
	ProcessPaymentPayload, ProcessPaymentInput,
	PaymentSummaryQuery, PaymentSummaryInput, PaymentSummaryOutput,
)

def new(payment_service: PaymentService) -> APIBlueprint:
	api = APIBlueprint(name='payment', import_name=__name__, logger=logger)
	handler = PaymentHandler(payment_service)

	@api.get('/payments-summary')
	@api.query(PaymentSummaryQuery)
	@api.response(200, PaymentSummaryOutput)
	def payments_summary(data: PaymentSummaryInput):
		return handler.payments_summary(data)

	@api.post('/payments')
	@api.payload(ProcessPaymentPayload)
	@api.response(201)
	def process_payment(data: ProcessPaymentInput):
		return handler.process_payment(data)

	return api
