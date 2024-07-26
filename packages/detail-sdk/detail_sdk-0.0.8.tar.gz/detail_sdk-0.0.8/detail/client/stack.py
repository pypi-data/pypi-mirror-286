_D='ddtrace/'
_C='segment/'
_B='python[^/]+/logging/'
_A='opentelemetry'
import inspect,re,threading
IGNORED_INSTRUMENTATION_CALLER_PATTERNS=[re.compile(A)for A in[_A,_B,_C,_D]]
IGNORED_INTERCEPTION_CALLER_PATTERNS=[re.compile(A)for A in[_A,_B,_C,_D,'[c|C]overage']]
def _is_in_patterns(s,patterns):
	for B in patterns:
		A=B.search(s)
		if A:return A
def get_thread_name():return threading.current_thread().name
def in_ignored_thread():A=get_thread_name();return A=='OtelBatchSpanProcessor'
def is_ignored_instrumentation_caller(caller_path):return in_ignored_thread()or _is_in_patterns(caller_path,IGNORED_INSTRUMENTATION_CALLER_PATTERNS)
def is_ignored_interception_caller(caller_path):return in_ignored_thread()or _is_in_patterns(caller_path,IGNORED_INTERCEPTION_CALLER_PATTERNS)
def get_caller_path(depth=1):
	B='site-packages';A,*C=get_caller_frameinfo(depth+1)
	if B in A:A=''.join(A.split(B)[1:]);A=A[1:]
	return A
def get_caller_frameinfo(depth=1):
	B=depth;B+=1;A=inspect.currentframe()
	for C in range(B):A=A.f_back
	try:return inspect.getframeinfo(A)
	finally:del A
def print_caller_frame(callee,depth=1):A,D,B,C,E=get_caller_frameinfo(depth+1);print('>',callee,'caller','/'.join(A.split('/')[-3:]),B,C[0].strip())