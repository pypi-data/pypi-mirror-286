_A=None
import wrapt
def get_psycopg2_extensions(psycopg_module):
	D='quote_ident';C='register_type';A=psycopg_module;B=[(A.extensions.register_type,A.extensions,C,_extensions_register_type),(A._psycopg.register_type,A._psycopg,C,_extensions_register_type),(A.extensions.adapt,A.extensions,'adapt',_extensions_adapt)]
	if getattr(A,'_json',_A):B+=[(A._json.register_type,A._json,C,_extensions_register_type)]
	if getattr(A,'extensions',_A)and getattr(A.extensions,D,_A):B+=[(A.extensions.quote_ident,A.extensions,D,_extensions_quote_ident)]
	return B
def _extensions_register_type(func,_,args,kwargs):
	def C(obj,scope=_A):return obj,scope
	B,A=C(*args,**kwargs)
	if A and isinstance(A,wrapt.ObjectProxy):A=A.__wrapped__
	return func(B,A)if A else func(B)
def _extensions_quote_ident(func,_,args,kwargs):
	def C(obj,scope=_A):return obj,scope
	B,A=C(*args,**kwargs)
	if A and isinstance(A,wrapt.ObjectProxy):A=A.__wrapped__
	return func(B,A)if A else func(B)
def _extensions_adapt(func,_,args,kwargs):
	A=func(*args,**kwargs)
	if hasattr(A,'prepare'):return AdapterWrapper(A)
	return A
class AdapterWrapper(wrapt.ObjectProxy):
	def prepare(E,*A,**C):
		D=E.__wrapped__.prepare
		if not A:return D(*A,**C)
		B=A[0]
		if isinstance(B,wrapt.ObjectProxy):B=B.__wrapped__
		return D(B,*A[1:],**C)
def _patch_extensions(_extensions):
	for(D,A,B,C)in _extensions:
		if not hasattr(A,B)or isinstance(getattr(A,B),wrapt.ObjectProxy):continue
		wrapt.wrap_function_wrapper(A,B,C)
def _unpatch_extensions(_extensions):
	for(A,B,C,D)in _extensions:setattr(B,C,A)