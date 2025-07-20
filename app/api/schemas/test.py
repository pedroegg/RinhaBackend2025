from marshmallow import fields
from typing import TypedDict

from library.flask_utils import BaseSchema as Schema

class TestQuery(Schema):
	delay = fields.Integer(data_key='delay', load_only=True, required=True)

class TestInput(TypedDict):
	delay: int
