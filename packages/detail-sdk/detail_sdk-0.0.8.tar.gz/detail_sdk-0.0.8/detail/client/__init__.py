import importlib.metadata,importlib.util,os
from pathlib import Path
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.id_generator import RandomIdGenerator
from opentelemetry.trace.span import format_trace_id
from detail.client import constants
from detail.client.logs import get_detail_logger
output_dir_path=Path(os.environ.get('__DETAIL_OUTPUT_DIR','.'))
logger=get_detail_logger(__name__)
try:version=importlib.metadata.version('detail-sdk')
except Exception:logger.warning("couldn't read package version",exc_info=True);version='unknown'
def instrument(api_key=None):
	D='true';B=api_key
	for E in load_instrumentor_classes():E().instrument()
	logger.info('all instrumentors installed');from detail.client.otel import JsonLSpanExporter as F,OTLPJsonHttpExporter as G;H=f"0x{format_trace_id(RandomIdGenerator().generate_trace_id())}";I=os.environ.get('__DETAIL_DEV','').lower()==D;J=os.environ.get('__DETAIL_USE_LOCAL_BACKEND','').lower()==D;A=None;B=B or os.environ.get('DETAIL_API_KEY')
	if B:
		if J:C=constants.LOCAL_BACKEND_URL
		else:C=constants.PROD_BACKEND_URL
		A=G(endpoint=f"{C}/v1/traces",headers={constants.PREFLIGHT_CUSTOMER_HEADER:B,constants.PREFLIGHT_VERSION_HEADER:version,constants.PREFLIGHT_CLIENT_LIBRARY_HEADER:'python',constants.PREFLIGHT_SERVICE_START_ID_HEADER:H})
	elif I:A=F(output_dir_path/'spans.jsonl')
	else:logger.warning('No Detail API key set. Use instrument(api_key=) or the DETAIL_API_KEY env var to send traces to the Detail backend.')
	trace.set_tracer_provider(TracerProvider(shutdown_on_exit=True))
	if A:K=BatchSpanProcessor(A,max_export_batch_size=10);trace.get_tracer_provider().add_span_processor(K);logger.debug('configured exporter %s',A)
	from detail.client.instrumentation.env import EnvInstrumentor as L;L.record_env()
instrumentor_defs=[('times.TimeInstrumentor',[]),('times.DatetimeInstrumentor',[]),('random.OSRandomInstrumentor',[]),('random.SystemRandomInstrumentor',[]),('random.RandomInstrumentor',[]),('uuid.UUIDInstrumentor',[]),('env.EnvInstrumentor',[]),('http2.Http2Instrumentor',[]),('sqlite3.SQLite3Instrumentor',[]),('redis.RedisInstrumentor',['redis']),('psycopg2.Psycopg2Instrumentor',['psycopg2']),('flask.DetailFlaskInstrumentor',['flask']),('django.DetailDjangoInstrumentor',['django']),('celery.CeleryInstrumentor',['celery'])]
def load_instrumentor_classes():
	for(C,D)in instrumentor_defs:
		E='detail.client.instrumentation.'+C;F,A=E.rsplit('.',1)
		for B in D:
			G=importlib.util.find_spec(B)
			if not G:logger.info('not loading %s due to missing %s',A,B);break
		else:H=importlib.import_module(F);I=getattr(H,A);yield I
__all__=[str(A)for A in[instrument]]