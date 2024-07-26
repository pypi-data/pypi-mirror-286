import json
from typing import Any,Callable,Dict
import forbiddenfruit
from opentelemetry.trace import Tracer
from wrapt.wrappers import _FunctionWrapperBase
from detail.client import stack
from detail.client.instrumentation.base import DisableDetail,RecursionTracker
from detail.client.serialization import DetailEncoder
NS='preflight'
def get_attributes(library,qualname,args,kwargs,result,empty_args=False):D=empty_args;C=kwargs;B=args;A=library;B,C=(tuple(),{})if D else(B,C);return{f"{NS}.library":A,f"{NS}.{A}.qualname":qualname,f"{NS}.{A}.args":json.dumps(B,cls=DetailEncoder),f"{NS}.{A}.kwargs":json.dumps(C,cls=DetailEncoder),f"{NS}.{A}.emptied":D,f"{NS}.{A}.return":json.dumps(result,cls=DetailEncoder)}
def get_pure_wrapper(tracer,library,empty_args=False):
	E=library
	def A(wrapped,instance,args,kwargs):
		C=kwargs;B=args;A=wrapped
		if DisableDetail.is_disabled():return A(*B,**C)
		D=f"{E}.{A.__qualname__}"
		if RecursionTracker.is_recursing(D):
			with DisableDetail():return A(*B,**C)
		H=stack.get_caller_path()
		if stack.is_ignored_instrumentation_caller(H):
			with DisableDetail():return A(*B,**C)
		with RecursionTracker(D):
			with tracer.start_as_current_span(D)as F:
				G=A(*B,**C)
				if F.is_recording():
					I=get_attributes(E,A.__qualname__,B,C,G,empty_args)
					for(J,K)in I.items():F.set_attribute(J,K)
				return G
	return A
class CopyableFunctionWrapperBase(_FunctionWrapperBase):
	def __copy__(A):return A
	def __deepcopy__(A,*B,**C):return A
def force_function_wrapper(target,name,wrapper,binding):C=binding;B=name;A=target;assert C in['function','classmethod','staticmethod'];D=getattr(A,B);E=A;F=getattr(A,'__dict__')[B];G=CopyableFunctionWrapperBase(D,E,wrapper,binding=C,parent=F);forbiddenfruit.curse(A,B,G)