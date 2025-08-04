import logging
logger = logging.getLogger("Payment router")

from library.flask_utils import APIBlueprint
from library.errors import BaseError, InternalError, BadRequest

from api.handlers import payment as handler
from api.schemas.payment import (
	ProcessPaymentPayload, ProcessPaymentInput,
	PaymentSummaryQuery, PaymentSummaryInput, PaymentSummaryOutput,
)

api = APIBlueprint(name='payment', import_name=__name__, logger=logger)

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
