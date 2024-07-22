from __future__ import annotations
import gc,json
from io import BytesIO
from typing import TYPE_CHECKING,Any
from urllib.parse import urlparse
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.trace import Span
from detail.client.instrumentation import NS
from detail.client.serialization import DetailEncoder
if TYPE_CHECKING:from django.http import HttpRequest,HttpResponse
class DetailDjangoInstrumentor(DjangoInstrumentor):
	def _instrument(B,**A):A['request_hook']=B.request_hook;A['response_hook']=B.response_hook;super()._instrument(**A)
	@staticmethod
	def request_hook(span,request):
		D='http.url';B=request;A=span;C=B._stream.read();B._stream=BytesIO(C);A.set_attribute('http.request.body',C);A.set_attribute(f"{NS}.library",'http')
		if D in A.attributes:A.set_attribute('http.target',urlparse(A.attributes[D]).path)
		A.set_attribute('http.request.headers',json.dumps(list(B.headers.items()),cls=DetailEncoder))
	@staticmethod
	def response_hook(span,request,response):
		D='http.route';B=response;A=span;A.set_attribute('http.status_code',B.status_code);C=list(B.headers.items());C.extend([('Set-Cookie',A.output(header=''))for A in B.cookies.values()])
		if D in A.attributes:A.set_attribute('http.request.path',A.attributes[D])
		A.set_attribute('http.response.headers',json.dumps(C,cls=DetailEncoder));A.set_attribute('http.response.body',B.content);gc.collect()