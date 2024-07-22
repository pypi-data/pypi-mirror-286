import datetime,time
from typing import Collection
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.trace import get_tracer
from wrapt import wrap_function_wrapper
from detail.client.instrumentation import force_function_wrapper,get_pure_wrapper
class TimeInstrumentor(BaseInstrumentor):
	time_functions=['time','monotonic','perf_counter','localtime','gmtime','time_ns','monotonic_ns','perf_counter_ns']
	def instrumentation_dependencies(A):return[]
	def _instrument(B,**D):
		C=get_tracer(__name__)
		for A in B.time_functions:
			if hasattr(time,A):wrap_function_wrapper(time,A,get_pure_wrapper(C,'time'))
	def _uninstrument(A,**B):0
class DatetimeInstrumentor(BaseInstrumentor):
	datetime_methods=['now','utcnow']
	def instrumentation_dependencies(A):return[]
	def _instrument(A,**D):
		B=get_tracer(__name__)
		for C in A.datetime_methods:force_function_wrapper(datetime.datetime,C,get_pure_wrapper(B,'datetime'),'classmethod')
	def _uninstrument(A,**B):0