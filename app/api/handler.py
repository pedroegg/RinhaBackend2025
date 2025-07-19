import logging
logger = logging.getLogger('Handler')

import json
import uuid
from datetime import datetime

import flask
from flask import request, Response

import library.errors as errors

def process_payment() -> Response:
	"""
	{
		"correlationId": "4a7901b8-7d26-4d9d-aa19-4dc1c7cf60b3",
		"amount": 19.90
	}

	no need to return body
	status_code 200
	"""

	res = flask.make_response()
	res.content_type = 'application/json; charset=utf-8'
	res.status_code = 200
	return res

def payments_summary() -> Response:
	"""
	Querystring params 'from' and 'to' (optional)
	from=2020-07-10T12:34:56.000Z&to=2020-07-10T12:35:56.000Z

	the return must be a json
	{
		"default" : {
			"totalRequests": 43236,
			"totalAmount": 415542345.98
		},
		"fallback" : {
			"totalRequests": 423545,
			"totalAmount": 329347.34
		}
	}
	all fields are required
	"""

	res = flask.make_response()
	res.content_type = 'application/json; charset=utf-8'
	res.status_code = 200
	return res





"""
def NewPessoa() -> Response:
	data = request.get_json(silent=True) #always consume body json data

	if not request.is_json:
		raise errors.BadRequest('the request body must be a json')

	if data is None:
		raise errors.BadRequest('invalid json')

	for field in ['apelido', 'nome', 'nascimento']:
		if not field in data or data[field] is None:
			raise errors.UnprocessableEntity(f'missing "{field}" field')

		if not isinstance(field, str):
			raise errors.BadRequest(f'field "{field}" must be a string')

	if 'stack' in data:
		if not isinstance(data['stack'], list):
			raise errors.BadRequest('field "stack" must be a list of strings')

		for stack in data['stack']:
			if not isinstance(stack, str):
				raise errors.BadRequest('field "stack" must be a list of strings')

			if len(stack) > STACK_MAX_LENGTH:
				raise errors.UnprocessableEntity(f'stacks must not have more than {STACK_MAX_LENGTH} characters')

	if len(data['apelido']) > APELIDO_MAX_LENGTH:
		raise errors.UnprocessableEntity(f'"apelido" field must not have more than {APELIDO_MAX_LENGTH} characters')

	if len(data['nome']) > NOME_MAX_LENGTH:
		raise errors.UnprocessableEntity(f'"nome" field must not have more than {NOME_MAX_LENGTH} characters')

	try:
		nascimento = datetime.strptime(data['nascimento'], '%Y-%m-%d').date()
	except ValueError:
		raise errors.BadRequest('"nascimento" field must be a date in the yyyy-mm-dd format')

	try:
		pessoa_id = PessoaService.Create(data['apelido'], data['nome'], nascimento, data['stack'])
	except:
		raise

	res = flask.make_response()
	res.content_type = 'application/json; charset=utf-8'
	res.status_code = 201
	res.headers.add('Location', f'/pessoas/{pessoa_id}')

	return res

def GetPessoaByID(id: str) -> Response:
	try:
		uuid.UUID(id, version=1)
	except ValueError:
		raise errors.NotFound(f'pessoa with id "{id}" not found') #change it later

	try:
		pessoa = PessoaService.GetByID(id)
	except:
		raise

	res = flask.make_response()
	res.content_type = 'application/json; charset=utf-8'
	res.status_code = 200
	res.set_data(json.dumps(pessoa, ensure_ascii=False, default=Pessoa.serializer))

	return res
"""
