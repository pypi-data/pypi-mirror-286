import logging,os
from logging.config import dictConfig
from detail.client.instrumentation.base import DisableDetail
class VCRStubsFilter(logging.Filter):
	def filter(D,record):
		C='http: %s';A=record;B=get_detail_logger('detail.vcr')
		if A.msg.startswith('Playing response for'):B.debug(C,A.msg)
		if A.msg.endswith('sending to real server'):B.debug(C,A.msg)
		return True
def init():
	N='propagate';M='level';L='vcr_stubs_filter';K='logging.StreamHandler';J='formatter';I='class';H='console_verbose';G='format';F='withfile';E='simple';D='filters';C='handlers';B=False;A=os.environ.get('DETAIL_LOG_LEVEL')
	if A:dictConfig({'version':1,'disable_existing_loggers':B,'formatters':{E:{G:'%(levelname)s: [%(asctime)s] %(name)s: %(message)s'},F:{G:'%(levelname)s: [%(asctime)s] (%(module)s:%(lineno)s): %(message)s'}},C:{'console_simple':{I:K,J:E},H:{I:K,J:F}},D:{L:{'()':VCRStubsFilter}},'loggers':{'detail':{C:[H],M:A,N:B},'vcr.stubs':{N:B,M:'INFO',D:[L]}}});get_detail_logger(__name__).info('detail logging enabled at level %s',A)
class DetailLogger(logging.Logger):
	def _log(C,*A,**B):
		with DisableDetail():return super()._log(*A,**B,stacklevel=2)
def get_detail_logger(*B,**C):A=logging.Logger.manager;D=A.loggerClass;A.loggerClass=DetailLogger;E=logging.getLogger(*B,**C);A.loggerClass=D;return E