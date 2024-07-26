def get_client():
	try:from sentry_sdk import Hub as A
	except ImportError:return
	return A.current.client
def flush():
	A=get_client()
	if A is not None:A.flush()
def close():
	A=get_client()
	if A is not None:A.close()