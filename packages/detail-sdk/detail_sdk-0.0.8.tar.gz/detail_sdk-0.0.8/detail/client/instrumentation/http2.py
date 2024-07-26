_C='external-http'
_B='connect'
_A=None
import json
from http.client import HTTPConnection,HTTPResponse,HTTPSConnection
from io import BytesIO
from typing import Collection
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.trace import get_tracer
from opentelemetry.trace.span import format_span_id
from wrapt import ObjectProxy,wrap_function_wrapper
from detail.client import stack
from detail.client.instrumentation import NS
from detail.client.instrumentation.base import DisableDetail
from detail.client.logs import get_detail_logger
from detail.client.serialization import DetailEncoder
try:from urllib3.connection import HTTPConnection as HTTPConnectionUrllib3,HTTPSConnection as HTTPSConnectionUrllib3
except ImportError:HTTPConnectionUrllib3,HTTPSConnectionUrllib3=_A,_A
logger=get_detail_logger(__name__)
def endheaders_wrapper(wrapped,instance,args,kwargs):
	res=wrapped(*args,**kwargs)
	if DisableDetail.is_disabled():return res
	caller_path=stack.get_caller_path()
	if stack.is_ignored_instrumentation_caller(caller_path):return res
	socket_proxy=instance.sock;request_data=b''.join(socket_proxy._self_buffer)
	with get_tracer('http').start_as_current_span(f"{instance._method} {instance.host} {instance.port}")as span:span.set_attribute(f"{NS}.library",_C);span.set_attribute(f"{NS}.external-http.method",instance._method);span.set_attribute(f"{NS}.external-http.host",instance.host);span.set_attribute(f"{NS}.external-http.port",instance.port);span.set_attribute(f"{NS}.external-http.request",json.dumps(request_data,cls=DetailEncoder));instance._detail_request_span_id=span.get_span_context().span_id
	return res
def getresponse_wrapper(wrapped,instance,args,kwargs):
	if DisableDetail.is_disabled():return wrapped(*args,**kwargs)
	caller_path=stack.get_caller_path()
	if stack.is_ignored_instrumentation_caller(caller_path):return wrapped(*args,**kwargs)
	orig_response_class=instance.response_class
	class ConnectionResponse(instance.response_class):
		def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self._connection=instance
	instance.response_class=ConnectionResponse;res=wrapped(*args,**kwargs);instance.response_class=orig_response_class;return res
def begin_wrapper(wrapped,instance,args,kwargs):
	if DisableDetail.is_disabled():return wrapped(*args,**kwargs)
	caller_path=stack.get_caller_path()
	if stack.is_ignored_instrumentation_caller(caller_path):return wrapped(*args,**kwargs)
	connection=getattr(instance,'_connection',_A)
	if connection is _A:logger.warning('failed to patch through _connection; not tracing response');return wrapped(*args,**kwargs)
	if getattr(connection,'_detail_request_span_id',_A)is _A:logger.warning("getresponse span id wasn't available; not tracing response");return wrapped(*args,**kwargs)
	buffered_fp=BufferingProxy(instance.fp);instance.fp=buffered_fp;result=wrapped(*args,**kwargs);header_data=b''.join(buffered_fp._self_buffer);instance.fp=buffered_fp.__wrapped__;body_length=instance.length;response_data=instance.read();instance.length=body_length;instance.fp=BytesIO(response_data);raw_response=header_data+response_data
	with get_tracer('http').start_as_current_span(f"{connection._method} {connection.host} {connection.port}")as span:span.set_attribute(f"{NS}.library",_C);span.set_attribute(f"{NS}.external-http.request_span_id",f"0x{format_span_id(connection._detail_request_span_id)}");span.set_attribute(f"{NS}.external-http.response",json.dumps(raw_response,cls=DetailEncoder))
	return result
class BufferingProxy(ObjectProxy):
	def __init__(self,wrapped):super().__init__(wrapped);self._self_buffer=[]
	def sendall(self,data):self._self_buffer.append(data);return self.__wrapped__.sendall(data)
	def readline(self,*args,**kwargs):r=self.__wrapped__.readline(*args,**kwargs);self._self_buffer.append(r);return r
def connect_wrapper(wrapped,instance,args,kwargs):
	with DisableDetail():res=wrapped(*args,**kwargs)
	if DisableDetail.is_disabled():return res
	caller_path=stack.get_caller_path()
	if stack.is_ignored_instrumentation_caller(caller_path):return res
	socket_proxy=BufferingProxy(instance.sock);instance.sock=socket_proxy;return res
class Http2Instrumentor(BaseInstrumentor):
	httplib_connection_methods=['endheaders',_B,'getresponse'];httplib_httpsconnection_methods=[_B];urllib3_connection_methods=[_B];httpresponse_methods=['begin']
	def instrumentation_dependencies(self):return[]
	def _instrument(self,**kwargs):
		A='_wrapper'
		for method in self.httplib_connection_methods:wrapper=globals()[method+A];wrap_function_wrapper(HTTPConnection,method,wrapper)
		for method in self.httplib_httpsconnection_methods:wrapper=globals()[method+A];wrap_function_wrapper(HTTPSConnection,method,wrapper)
		for method in self.httpresponse_methods:wrapper=globals()[method+A];wrap_function_wrapper(HTTPResponse,method,wrapper)
		if HTTPConnectionUrllib3:
			for method in self.urllib3_connection_methods:wrapper=globals()[method+A];wrap_function_wrapper(HTTPConnectionUrllib3,method,wrapper);wrap_function_wrapper(HTTPSConnectionUrllib3,method,wrapper)
	def _uninstrument(self,**kwargs):0