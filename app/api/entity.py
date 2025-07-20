from dataclasses import dataclass
from decimal import Decimal

@dataclass
class PaymentSummaryItem:
	requests_number: int
	total_amount: Decimal

@dataclass
class PaymentSummaryEntity:
	default: PaymentSummaryItem
	fallback: PaymentSummaryItem
