import logging
logger = logging.getLogger("Router")

from flask import make_response, Response
from flask_smorest import Blueprint
from marshmallow.exceptions import ValidationError

import json
import requests

import api.handler as Handler
from api.schema import (
	ProcessPaymentPayload, ProcessPaymentInput,
	PaymentSummaryArgs, PaymentSummaryInput, PaymentSummaryOutput
)
from library.errors import BaseError, InternalError, BadRequest

api = Blueprint('api', __name__)

# ------------ API Routes ------------

@api.get('/payments-summary')
@api.arguments(PaymentSummaryArgs, location='query')
@api.response(200, PaymentSummaryOutput)
def payments_summary(payload: PaymentSummaryInput):
	return Handler.payments_summary(payload)

@api.post('/payments')
@api.arguments(ProcessPaymentPayload, location='json')
@api.response(201)
def process_payment(payload: ProcessPaymentInput):
	return Handler.process_payment(payload)

@api.get('/test')
@api.response(200)
def test_request():
	return requests.get('https://httpbin.org/delay/5').json()

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