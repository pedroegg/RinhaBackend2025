from marshmallow import fields
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import TypedDict

from library.flask_utils import BaseSchema as Schema

class ProcessPaymentPayload(Schema):
	correlation_id = fields.UUID(data_key='correlationId', load_only=True, required=True, allow_none=False)
	amount = fields.Decimal(places=2, data_key='amount', load_only=True, required=True, allow_none=False)

class ProcessPaymentInput(TypedDict):
	correlation_id: UUID
	amount: Decimal

class PaymentSummaryQuery(Schema):
	start = fields.DateTime(format='iso', data_key='from', load_only=True, required=False)
	end = fields.DateTime(format='iso', data_key='to', load_only=True, required=False)

class PaymentSummaryInput(TypedDict):
	start: datetime
	end: datetime

class PaymentSummaryOutput(Schema):
	class _SummaryItem(Schema):
		requests_number = fields.Integer(data_key='totalRequests', dump_only=True, required=True)
		total_amount = fields.Decimal(places=2, data_key='totalAmount', dump_only=True, required=True)

	default = fields.Nested(_SummaryItem, data_key='default', dump_only=True, required=True)
	fallback = fields.Nested(_SummaryItem, data_key='fallback', dump_only=True, required=True)

class TestQuery(Schema):
	delay = fields.Integer(data_key='delay', load_only=True, required=True)

class TestInput(TypedDict):
	delay: int
