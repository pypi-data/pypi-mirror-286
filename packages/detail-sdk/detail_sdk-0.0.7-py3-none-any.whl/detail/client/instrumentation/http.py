import json
from typing import Collection
from urllib.parse import urlparse
import vcr
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.trace import get_tracer
from vcr.cassette import Cassette
from vcr.persisters.filesystem import CassetteNotFoundError
from vcr.record_mode import RecordMode
from vcr.serializers import compat
from wrapt import wrap_function_wrapper
from detail.client import constants,stack
from detail.client.instrumentation import NS
from detail.client.instrumentation.base import DisableDetail
from detail.client.logs import get_detail_logger
from detail.client.serialization import DetailEncoder
prod_url_components=urlparse(constants.PROD_BACKEND_URL)
local_url_components=urlparse(constants.LOCAL_BACKEND_URL)
logger=get_detail_logger(__name__)
def before_record_cb(request):
	A=request
	if DisableDetail.is_disabled():return
	if A.host.endswith('ingest.sentry.io'):logger.debug('ignoring sentry http request');return
	if A.host==prod_url_components.hostname:return
	if A.protocol==local_url_components.scheme and A.host==local_url_components.hostname and A.port==local_url_components.port:return
	B=stack.get_caller_path()
	if stack.is_ignored_instrumentation_caller(B)or stack.is_ignored_interception_caller(B):return
	return A
detail_vcr=vcr.VCR(before_record_request=before_record_cb)
def append_wrapper(wrapped,instance,args,kwargs):
	C=instance;D=wrapped(*args,**kwargs)
	if not C.data:return D
	A,E=C.data[-1];F=compat.convert_to_unicode(A._to_dict());G=compat.convert_to_unicode(E)
	with get_tracer('http').start_as_current_span(f"{A.method} {A.uri}")as B:B.set_attribute(f"{NS}.library",'external-http');B.set_attribute('external-http.request',json.dumps(F,cls=DetailEncoder));B.set_attribute('external-http.response',json.dumps(G,cls=DetailEncoder))
	return D
class NoopPersister:
	def load_cassette(A,cassette_path,serializer):raise CassetteNotFoundError()
	def save_cassette(A,cassette_path,cassette_dict,serializer):0
class HttpInstrumentor(BaseInstrumentor):
	cassette_manager=None
	def instrumentation_dependencies(A):return[]
	def _instrument(A,**B):detail_vcr.register_persister(NoopPersister());wrap_function_wrapper(Cassette,'append',append_wrapper);A.start_capturing_http()
	def _uninstrument(A,**B):0
	@classmethod
	def start_capturing_http(A):A.cassette_manager=detail_vcr.use_cassette('<detail span cassette>',record_mode=RecordMode.ALL);A.cassette_manager.__enter__()