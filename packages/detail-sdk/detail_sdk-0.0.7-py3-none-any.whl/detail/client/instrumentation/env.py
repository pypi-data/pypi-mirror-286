import json,os
from typing import Collection
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.trace import get_tracer
from detail.client.instrumentation import NS
from detail.client.serialization import DetailEncoder
class EnvInstrumentor(BaseInstrumentor):
	def instrumentation_dependencies(A):return[]
	def _instrument(C,**D):
		B=get_tracer(__name__)
		with B.start_as_current_span('environ')as A:A.set_attribute(f"{NS}.library",'env');A.set_attribute(f"{NS}.env.environ",json.dumps(dict(os.environ),cls=DetailEncoder))
	def _uninstrument(A,**B):0