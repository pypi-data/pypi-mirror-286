import logging,os
from logging.config import dictConfig
from detail.client.instrumentation.base import DisableDetail
def init():
	J='logging.StreamHandler';I='formatter';H='class';G='console_verbose';F='format';E='withfile';D='simple';C=False;B='handlers';A=os.environ.get('DETAIL_LOG_LEVEL')
	if A:dictConfig({'version':1,'disable_existing_loggers':C,'formatters':{D:{F:'%(levelname)s: [%(asctime)s] %(name)s: %(message)s'},E:{F:'%(levelname)s: [%(asctime)s] (%(module)s:%(lineno)s): %(message)s'}},B:{'console_simple':{H:J,I:D},G:{H:J,I:E}},'loggers':{'detail':{B:[G],'level':A,'propagate':C}}});get_detail_logger(__name__).info('detail logging enabled at level %s',A)
class DetailLogger(logging.Logger):
	def _log(C,*A,**B):
		with DisableDetail():return super()._log(*A,**B,stacklevel=2)
def get_detail_logger(*B,**C):A=logging.Logger.manager;D=A.loggerClass;A.loggerClass=DetailLogger;E=logging.getLogger(*B,**C);A.loggerClass=D;return E