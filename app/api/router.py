import logging
logger = logging.getLogger("Router")

from flask import make_response, Response
from marshmallow.exceptions import ValidationError
import json

import api.handler as handler
from api.schema import (
	ProcessPaymentPayload, ProcessPaymentInput,
	PaymentSummaryQuery, PaymentSummaryInput, PaymentSummaryOutput,
	TestQuery, TestInput,
)
from library.flask_utils import APIBlueprint
from library.errors import BaseError, InternalError, BadRequest

api = APIBlueprint('api', __name__)

# ------------ API Routes ------------

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

@api.get('/test')
@api.query(TestQuery)
@api.response(200)
def test_request(data: TestInput):
	return handler.test(data)

# ------------------------------------

# ---------- Error Handlers ----------

@api.errorhandler(BaseError)
def handle_error(e: BaseError) -> Response:
	payload = {
		'error': {
			'code': e.code,
			'name': e.name,
			'description': e.description,
		}
	}

	res = make_response()
	res.content_type = 'application/json; charset=utf-8'
	res.status_code = e.code
	res.set_data(json.dumps(payload, ensure_ascii=False))
	return res

@api.errorhandler(Exception)
def handle_exception(e: Exception) -> Response:
	if isinstance(e, ValidationError):
		return handle_error(BadRequest(e.normalized_messages()))

	logger.error(e, exc_info=1)
	return handle_error(InternalError(e.__str__()))

# ------------------------------------