import sqlite3
from sqlite3 import dbapi2
from typing import Collection
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from wrapt import wrap_function_wrapper
from detail.client.instrumentation.dbapi import TracedConnection,get_connect_wrapper
class SQLite3Instrumentor(BaseInstrumentor):
	def instrumentation_dependencies(A):return[]
	def _instrument(B,**C):
		for A in[sqlite3,dbapi2]:wrap_function_wrapper(A,'connect',get_connect_wrapper(TracedConnection,'sqlite3'))
	def _uninstrument(A,**B):0