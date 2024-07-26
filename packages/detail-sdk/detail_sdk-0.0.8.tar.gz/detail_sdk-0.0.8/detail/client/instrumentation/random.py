_A='random'
import os,random,secrets
from typing import Collection
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.trace import get_tracer
from wrapt import wrap_function_wrapper
from detail.client.instrumentation import get_pure_wrapper
class RandomInstrumentor(BaseInstrumentor):
	random_methods=[A for A in[_A,'getrandbits','randbytes']if getattr(random.Random,A,None)]
	def instrumentation_dependencies(A):return[]
	def _instrument(A,**D):
		B=get_tracer(__name__)
		for C in A.random_methods:wrap_function_wrapper(random.Random,C,get_pure_wrapper(B,_A))
		A.patch_module_funcs()
	def _uninstrument(A,**B):0
	@staticmethod
	def patch_module_funcs():
		B=random.Random()
		for A in dir(B):
			if not A.startswith('_')and hasattr(random,A):setattr(random,A,getattr(B,A))
class SystemRandomInstrumentor(BaseInstrumentor):
	def instrumentation_dependencies(A):return[]
	def _instrument(A,**D):
		B=get_tracer(__name__)
		for C in RandomInstrumentor.random_methods:wrap_function_wrapper(random.SystemRandom,C,get_pure_wrapper(B,'systemrandom'))
		A.patch_module_funcs()
	def _uninstrument(A,**B):0
	@staticmethod
	def patch_module_funcs():A=random.SystemRandom();secrets._sysrand=A;secrets.randbits=A.getrandbits;secrets.choice=A.choice
class OSRandomInstrumentor(BaseInstrumentor):
	random_functions=['getrandom','urandom']
	def instrumentation_dependencies(A):return[]
	def _instrument(A,**D):
		B=get_tracer(__name__)
		for C in A.random_functions:wrap_function_wrapper(os,C,get_pure_wrapper(B,'osrandom'))
		random._urandom=os.urandom
	def _uninstrument(A,**B):0