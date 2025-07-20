"""
Helpers to integrate Flask-smorest with schemas that accepts dataclasses.

- BaseSchema: Automatically converts dataclasses to dict when dumping.
- APIBlueprint: Wrapper/aliases with location already included.
"""

from flask import make_response, Response
from flask_smorest import Blueprint
from marshmallow import Schema, pre_dump
from marshmallow.exceptions import ValidationError
from dataclasses import asdict, is_dataclass
from collections.abc import Sequence
from typing import Any
from logging import Logger
import json
import os

from library.errors import BaseError, InternalError, BadRequest

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
	def __init__(
			self,
			name: str,
			import_name: str,
			logger: Logger | None = None,
			static_folder: str | os.PathLike[str] | None = None,
			static_url_path: str | None = None,
			template_folder: str | os.PathLike[str] | None = None,
			url_prefix: str | None = None,
			subdomain: str | None = None,
			url_defaults: dict[str, Any] | None = None,
			root_path: str | None = None,
		):
		"""Instantiate a new APIBlueprint with already configured error handlers."""

		super().__init__(
			name=name,
			import_name=import_name,
			static_folder=static_folder,
			static_url_path=static_url_path,
			template_folder=template_folder,
			url_prefix=url_prefix,
			subdomain=subdomain,
			url_defaults=url_defaults,
			root_path=root_path,
		)

		@self.errorhandler(BaseError)
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

		@self.errorhandler(Exception)
		def handle_exception(e: Exception) -> Response:
			if isinstance(e, ValidationError):
				return handle_error(BadRequest(e.normalized_messages()))

			if logger:
				logger.error(e, exc_info=1)

			return handle_error(InternalError(e.__str__()))

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
