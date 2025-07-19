import logging
logger = logging.getLogger("Router")

from flask import Blueprint, request, render_template
import json
import requests

import api.handler as Handler
from library.errors import InternalError, BaseError

api = Blueprint('api', __name__)

# ------------ API Routes ------------

@api.route('/payments', methods=['POST'])
def process_payment():
	return Handler.process_payment()

@api.route('/payments-summary', methods=['GET'])
def payments_summary():
	return Handler.payments_summary()

@api.route('/test', methods=['GET'])
def test_request():
	return requests.get('https://httpbin.org/delay/5').json()

# ------------------------------------

# ---------- Error Handlers ----------

@api.errorhandler(BaseError)
def handle_crafted_errors(e: BaseError):
	response = e.get_response()
	response.data = json.dumps({
		'error': {
			'code': e.code,
			'name': e.name,
			'description': e.description,
		},
	})
	response.content_type = 'application/json'
	response.charset = 'utf-8'

	return response

@api.errorhandler(Exception)
def handle_exception(e: Exception):
	logger.error(e, exc_info=1)
	return handle_crafted_errors(InternalError(e.__str__()))

# ------------------------------------

"""
@api.route('/pessoas/<string:id>', methods=['GET'])
def GetPessoaByID(id: str):
	return Handler.GetPessoaByID(id)

@api.route('/pessoas', methods=['GET'])
def FilterPessoas():
	return Handler.FilterPessoas()

@api.route('/contagem-pessoas', methods=['GET'])
def CountPessoas():
	return Handler.CountPessoas()
"""