_H='struct_time'
_G='initargs'
_F='builtin_type'
_E='iso8601'
_D='utf-8'
_C='utf8'
_B='tuple'
_A='Column'
import builtins,json,time
from base64 import b64decode,b64encode
from datetime import date,datetime,timedelta,timezone
from io import BytesIO
from typing import Any,Dict,Type
from uuid import UUID
psycopg2_types={_A:None}
try:import psycopg2.extensions
except ImportError:pass
else:
	for name in psycopg2_types:psycopg2_types[name]=getattr(psycopg2.extensions,name,None)
TYPE_KEY='__detail_json_type__'
known_lossy_type_strs={"<class 'dateutil.tz.tz.tzutc'>"}
LOSSY_REPR='lossy-repr'
builtin_types={A for A in builtins.__dict__.values()if isinstance(A,type)}
def decode_bytes(obj):
	A=obj
	if _C in A:return A[_C].encode(_D)
	else:return b64decode(A['b64'])
def encode_bytes(obj):
	B=obj;A={}
	try:A[_C]=B.decode(_D)
	except UnicodeDecodeError:A['b64']=b64encode(B).decode(_D)
	A[TYPE_KEY]=str(B.__class__.__name__);return A
def encode_psycopg2_type(type,obj):B=[A for A in dir(obj)if not A.startswith('_')];A={A:getattr(obj,A)for A in B};A[TYPE_KEY]=f"psycopg2.extensions.{type.__name__}";return A
class DetailEncoder(json.JSONEncoder):
	def default(H,obj):
		E='repr';C='type';A=obj;from detail.client.logs import get_detail_logger as F;G=F()
		try:hash(A)
		except TypeError:pass
		else:
			if A in builtin_types:B={'name':A.__name__};B[TYPE_KEY]=_F;return B
		if psycopg2_types[_A]and isinstance(A,psycopg2_types[_A]):return encode_psycopg2_type(psycopg2_types[_A],A)
		if isinstance(A,(datetime,date)):B={_E:A.isoformat()};B[TYPE_KEY]=str(A.__class__.__name__);return B
		if isinstance(A,timezone):assert hasattr(A,'__getinitargs__');B={_G:A.__getinitargs__()};B[TYPE_KEY]=str(A.__class__.__name__);return B
		if isinstance(A,timedelta):B={'days':A.days,'seconds':A.seconds,'microseconds':A.microseconds};B[TYPE_KEY]=str(A.__class__.__name__);return B
		if isinstance(A,bytes):return encode_bytes(A)
		if isinstance(A,UUID):B={'str':str(A)};B[TYPE_KEY]=str(A.__class__.__name__);return B
		if isinstance(A,memoryview):return encode_bytes(A.tobytes())
		if isinstance(A,BytesIO):return encode_bytes(A.read())
		try:D=super().default(A)
		except TypeError:
			B={C:str(type(A)),E:repr(A)};B[TYPE_KEY]=LOSSY_REPR
			if B[C]not in known_lossy_type_strs:G.warning("encoding %s with lossy repr '%s'; add serilization support or add to known_lossy_type_strs",B[C],B[E],stack_info=True)
			return B
		assert isinstance(D,dict);return D
	def encode(A,obj):
		def B(item):
			A=item
			if isinstance(A,time.struct_time):C={_B:B(tuple(A))};C[TYPE_KEY]=_H;return C
			elif isinstance(A,tuple):return{TYPE_KEY:_B,'items':[B(A)for A in A]}
			elif isinstance(A,list):return[B(A)for A in A]
			elif isinstance(A,dict):return{A:B(C)for(A,C)in A.items()}
			else:return A
		return super().encode(B(obj))
class DetailDecoder(json.JSONDecoder):
	def __init__(A,*B,**C):json.JSONDecoder.__init__(A,*B,object_hook=A.object_hook,**C)
	def object_hook(C,obj):
		A=obj;B=A.pop(TYPE_KEY,None)
		if B==_F:A=builtins.__dict__[A['name']]
		elif B=='psycopg2.extensions.Column':assert psycopg2_types[_A],'psycopg2 is required to deserialize Column; was detail installed with the replay extras?';A=psycopg2_types[_A](**A)
		elif B==_B:A=tuple(A['items'])
		elif B=='datetime':A=datetime.fromisoformat(A[_E])
		elif B=='date':A=date.fromisoformat(A[_E])
		elif B=='timezone':A=timezone(*A[_G])
		elif B=='timedelta':A=timedelta(**A)
		elif B==_H:A=time.struct_time(A[_B])
		elif B=='bytes':A=decode_bytes(A)
		elif B=='UUID':A=UUID(A['str'])
		elif B=='memoryview':A=memoryview(decode_bytes(A))
		elif B=='BytesIO':A=BytesIO(decode_bytes(A))
		elif B==LOSSY_REPR:A[TYPE_KEY]=B
		return A