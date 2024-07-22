_A='__call__'
import gc,json
from typing import Any
import flask
from flask import Response,request
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.utils import unwrap
from opentelemetry.trace import get_tracer
from wrapt import wrap_function_wrapper
from detail.client.instrumentation import NS
from detail.client.logs import get_detail_logger
from detail.client.serialization import DetailEncoder
logger=get_detail_logger(__name__)
def before_request():
	B='http.route';A=trace.get_current_span();A.set_attribute(f"{NS}.library",'http');A.set_attribute('http.request.body',request.get_data(as_text=True))
	if B in A.attributes:A.set_attribute('http.request.path',A.attributes[B])
	A.set_attribute('http.request.headers',json.dumps(request.headers.to_wsgi_list(),cls=DetailEncoder))
def after_request(response):A=response;B=trace.get_current_span();B.set_attribute('http.status_code',A.status_code);B.set_attribute('http.response.headers',json.dumps(A.headers.to_wsgi_list(),cls=DetailEncoder));B.set_attribute('http.response.body',A.data);gc.collect();return A
def call_wrapper(wrapped,instance,args,kwargs):
	A='wsgi'
	with get_tracer(A).start_as_current_span(A)as B:B.set_attribute(f"{NS}.library",A);return wrapped(*args,**kwargs)
def sentry_flask_setup_wrapper(wrapped,instance,args,kwargs):unwrap(flask.Flask,_A);A=wrapped(*args,**kwargs);wrap_function_wrapper(flask.Flask,_A,call_wrapper);logger.info('rewrapped flask around sentry');return A
class DetailFlaskInstrumentor(FlaskInstrumentor):
	def _instrument(D,**A):
		super()._instrument(**A)
		class B(flask.Flask):
			def __init__(A,*B,**C):super().__init__(*B,**C);A.before_request(before_request);A.after_request(after_request)
		flask.Flask=B;wrap_function_wrapper(flask.Flask,_A,call_wrapper)
		try:from sentry_sdk.integrations.flask import FlaskIntegration as C
		except ImportError:pass
		else:logger.info('sentry detected; monkeypatching FlaskIntegration.setup_once');wrap_function_wrapper(C,'setup_once',sentry_flask_setup_wrapper)