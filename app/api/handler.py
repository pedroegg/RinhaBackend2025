import logging
logger = logging.getLogger('Handler')

from flask import make_response
from dataclasses import asdict
from decimal import Decimal
import requests

from api.entity import PaymentSummaryEntity, PaymentSummaryItem
from api.schema import ProcessPaymentInput, PaymentSummaryInput, TestInput

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

def test(data: TestInput) -> None:
	requests.get(f'https://httpbin.org/delay/{data['delay']}')
