_A='cursor'
import json,wrapt
from opentelemetry.trace import get_tracer
from opentelemetry.trace.span import format_span_id
from detail.client.instrumentation import NS
from detail.client.logs import get_detail_logger
from detail.client.serialization import DetailEncoder
logger=get_detail_logger(__name__)
class TracedCursor(wrapt.ObjectProxy):
	def __init__(A,cursor,client,connection):super(TracedCursor,A).__init__(cursor);A._self_execute_span=None;A._self_client=client;A._self_connection=connection
	def __execute(B,function,query,*E,**F):
		D=query;C=function;logger.debug('execute %s %r %r %r',C,D,E,F);G=getattr(B.__wrapped__,C);H=G(D,*E,**F)
		with get_tracer(_A).start_as_current_span(C)as A:B._self_execute_span=A;A.set_attribute(f"{NS}.library",'dbapi');A.set_attribute(f"{NS}.dbapi.client",B._self_client);A.set_attribute(f"{NS}.dbapi.qualname",C);A.set_attribute(f"{NS}.dbapi.query",D);A.set_attribute(f"{NS}.dbapi.args",json.dumps(E,cls=DetailEncoder));A.set_attribute(f"{NS}.dbapi.kwargs",json.dumps(F,cls=DetailEncoder));I={'description':B.__wrapped__.description,'rowcount':B.__wrapped__.rowcount,'lastrowid':B.__wrapped__.lastrowid};A.set_attribute(f"{NS}.dbapi.execute_result",json.dumps(I,cls=DetailEncoder))
		if H:return B
	def execute(A,query,*B,**C):return A.__execute('execute',query,*B,**C)
	def executemany(A,query,*B,**C):return A.__execute('executemany',query,*B,**C)
	def callproc(A,proc,*B,**C):return A.__execute('callproc',proc,*B,**C)
	def __fetch(E,function,*C,**D):
		B=function;logger.debug('fetch %s %r %r',B,C,D);G=getattr(E.__wrapped__,B);F=G(*C,**D)
		with get_tracer(_A).start_as_current_span(B)as A:A.set_attribute(f"{NS}.library",'dbapi');A.set_attribute(f"{NS}.dbapi.qualname",B);A.set_attribute(f"{NS}.dbapi.args",json.dumps(C,cls=DetailEncoder));A.set_attribute(f"{NS}.dbapi.kwargs",json.dumps(D,cls=DetailEncoder));A.set_attribute(f"{NS}.dbapi.result",json.dumps(F,cls=DetailEncoder));A.set_attribute(f"{NS}.dbapi.execute_span_id",f"0x{format_span_id(E._self_execute_span.get_span_context().span_id)}")
		return F
	def fetchall(A):return A.__fetch('fetchall')
	def fetchone(A):return A.__fetch('fetchone')
	def fetchmany(A,*B,**C):return A.__fetch('fetchmany',*B,**C)
	def __iter__(A):return A
	def __next__(B):
		A=B.fetchone()
		if A is None:raise StopIteration
		return A
	next=__next__
class TracedConnection(wrapt.ObjectProxy):
	def __init__(A,conn,client):super(TracedConnection,A).__init__(conn);A._self_client=client
	def cursor(A,*B,**C):D=A.__wrapped__.cursor(*B,**C);return TracedCursor(D,A._self_client,A)
def get_connect_wrapper(traced_conn_cls,*A,**B):
	def C(wrapped,instance,args,kwargs):C=wrapped(*args,**kwargs);return traced_conn_cls(C,*A,**B)
	return C