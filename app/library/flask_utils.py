"""
Helpers to integrate Flask-smorest with schemas that accepts dataclasses.

- BaseSchema: Automatically converts dataclasses to dict when dumping.
- APIBlueprint: Wrapper/aliases with location already included.
"""

from flask_smorest import Blueprint
from marshmallow import Schema, pre_dump
from dataclasses import asdict, is_dataclass
from collections.abc import Sequence
from typing import Any

__all__ = ["BaseSchema", "APIBlueprint"]

class BaseSchema(Schema):
	@pre_dump
	def _dataclass_to_dict(self, obj: Any, **_: Any) -> Any:
		if is_dataclass(obj):
			return asdict(obj)

		if isinstance(obj, Sequence) and obj and is_dataclass(obj[0]):
			return [asdict(o) for o in obj]

		return obj

class APIBlueprint(Blueprint):
	def header(self, schema: BaseSchema, description: str | None = None):
		"""Register a schema definition for HTTP headers."""
		return super().arguments(schema, location='header', description=description)

	def cookie(self, schema: BaseSchema, description: str | None = None):
		"""Register a schema definition for HTTP cookies."""
		return super().arguments(schema, location='cookies', description=description)

	def query(self, schema: BaseSchema, description: str | None = None):
		"""Register a schema definition for URL querystrings (e.g.: ?a=1&b=2)."""
		return super().arguments(schema, location='query', description=description)

	def arg(self, schema: BaseSchema, description: str | None = None):
		"""Register a schema definition for URL path params (e.g.: /users/<id>)."""
		return super().arguments(schema, location='path', description=description)

	def form(self, schema: BaseSchema, description: str | None = None):
		"""Register a schema definition for a form (application/x-www-form-urlencoded)."""
		return super().arguments(schema, location='form', description=description)

	def file(self, schema: BaseSchema, description: str | None = None):
		"""Register a schema definition for multipart/form data."""
		return super().arguments(schema, location='files', description=description)

	def payload(self, schema: BaseSchema, description: str | None = None):
		"""Register a schema definition for a JSON payload."""
		return super().arguments(schema, location='json', description=description)

	def response(self, status_code: int, schema: BaseSchema | None = None, description: str | None = None):
		"""Register a schema definition for the request response."""
		return super().response(status_code, schema, description=description)
