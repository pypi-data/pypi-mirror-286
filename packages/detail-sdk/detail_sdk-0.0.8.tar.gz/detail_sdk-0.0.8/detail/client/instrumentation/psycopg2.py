_B='psycopg2-conninfo'
_A='psycopg2'
from typing import Collection
import psycopg2,wrapt
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.trace import get_tracer
from wrapt import wrap_function_wrapper
from detail.client.instrumentation import ddpsycopg2,get_pure_wrapper
from detail.client.instrumentation.dbapi import TracedConnection,get_connect_wrapper
from detail.client.logs import get_detail_logger
logger=get_detail_logger(__name__)
class TracedConnectionInfo(wrapt.ObjectProxy):
	def __getattr__(C,name):
		A=name;B=super().__getattr__(A)
		if A.startswith('_'):return B
		if callable(B):D=wrapt.decorator(get_pure_wrapper(get_tracer(_B),_A));return D(B)
		else:return C.conninfo_attr(A)
	@wrapt.decorator(get_pure_wrapper(get_tracer(_B),_A))
	def conninfo_attr(self,name):return super().__getattr__(name)
class Psycopg2TracedConnection(TracedConnection):
	@property
	def info(self):A=self.__wrapped__.info;return TracedConnectionInfo(A)
class Psycopg2Instrumentor(BaseInstrumentor):
	def instrumentation_dependencies(A):return[]
	def instrument(C,*B,**A):A['skip_dep_check']=True;return super().instrument(*B,**A)
	def _instrument(B,**C):A=ddpsycopg2.get_psycopg2_extensions(psycopg2);ddpsycopg2._patch_extensions(A);wrap_function_wrapper(psycopg2,'connect',get_connect_wrapper(Psycopg2TracedConnection,_A))
	def _uninstrument(A,**B):0