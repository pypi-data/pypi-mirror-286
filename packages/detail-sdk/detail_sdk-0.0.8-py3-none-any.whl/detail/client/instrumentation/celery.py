_B='celery'
_A='empty_args'
from typing import Collection
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.trace import get_tracer
from wrapt import wrap_function_wrapper
from detail.client.instrumentation import get_pure_wrapper
class CeleryInstrumentor(BaseInstrumentor):
	targets=[('kombu.common','oid_from',{_A:True}),('celery.utils.nodenames','anon_nodename',{_A:True})]
	def instrumentation_dependencies(A):return[_B]
	def _instrument(A,**F):
		B=get_tracer(__name__)
		for(C,D,E)in A.targets:wrap_function_wrapper(C,D,get_pure_wrapper(B,_B,**E))
	def _uninstrument(A,**B):0