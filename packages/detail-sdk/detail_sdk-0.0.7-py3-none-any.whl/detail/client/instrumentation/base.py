_A=False
import threading
from contextlib import ContextDecorator
from typing import Any,Optional,Type
class DisableDetail(ContextDecorator):
	threadlocal=threading.local()
	def __enter__(A):A.threadlocal.disabled=True
	def __exit__(A,exc_type,exc_value,exc_traceback):A.threadlocal.disabled=_A
	@classmethod
	def is_disabled(A):return getattr(A.threadlocal,'disabled',_A)
class RecursionTracker:
	threadlocal=threading.local()
	def __init__(A,id):A.id=id
	@classmethod
	def is_recursing(A,id):return bool(A.threadlocal.__dict__.get(id,_A))
	def __enter__(A):A.threadlocal.__dict__[A.id]=True
	def __exit__(A,exc_type,exc_value,exc_traceback):del A.threadlocal.__dict__[A.id]