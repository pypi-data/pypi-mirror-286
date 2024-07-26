import json
from os.path import isfile
from threading import Lock
import requests.exceptions
from google.protobuf.json_format import MessageToJson
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter,_create_exp_backoff_generator,encode_spans,sleep
from opentelemetry.sdk.trace.export import SpanExporter,SpanExportResult
from detail.client.instrumentation.base import DisableDetail
from detail.client.logs import get_detail_logger
logger=get_detail_logger(__name__)
class OTLPJsonHttpExporter(OTLPSpanExporter):
	def __init__(A,*B,**C):super().__init__(*B,**C);A._session.headers.update({'content-type':'application/json'});A._MAX_RETRY_TIMEOUT=30
	@DisableDetail()
	def export(self,spans):
		B=self
		if B._shutdown:return SpanExportResult.FAILURE
		D=MessageToJson(encode_spans(spans),use_integers_for_enums=True)
		for C in _create_exp_backoff_generator(max_value=B._MAX_RETRY_TIMEOUT):
			if C==B._MAX_RETRY_TIMEOUT:logger.error('Failed to export batch after hitting max retries');return SpanExportResult.FAILURE
			try:A=B._export(D)
			except requests.exceptions.ConnectionError:logger.info('Connection error, retrying in %ss.',C);sleep(C);continue
			if A.ok:return SpanExportResult.SUCCESS
			elif A.status_code!=500 and B._retryable(A):logger.warning('Transient status code %s encountered while exporting span batch, retrying in %ss.',A.status_code,C);sleep(C);continue
			else:logger.error('Failed to export batch code: %s, response: %r',A.status_code,A.text);return SpanExportResult.FAILURE
		return SpanExportResult.FAILURE
class JsonLSpanExporter(SpanExporter):
	@DisableDetail()
	def __init__(self,output_path):
		A=self;super().__init__();A.output_path=output_path;A.lock=Lock()
		if isfile(A.output_path):raise RuntimeError(f"{A.output_path} must be empty to be used as an export file")
	@DisableDetail()
	def export(self,spans):
		G='resource';F='kind';E='context';C=[]
		for B in spans:A=json.loads(B.to_json());A['traceId']=A[E]['trace_id'];A['parentId']=A['parent_id'];A['id']=A[E]['span_id'];A['kind_str']=A[F];A[F]=B.kind.value;A['timestamp']=int(B._start_time/1000);A['duration']=(B._end_time-B._start_time)/1000;A[G]['_attributes']=A[G].pop('attributes');C.append(A)
		with self.lock:
			with open(self.output_path,'a')as D:
				for B in C:json.dump(B,D);D.write('\n')
		return SpanExportResult.SUCCESS