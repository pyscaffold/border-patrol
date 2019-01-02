import logging
from . import BorderPatrol

BorderPatrol(report_fun=logging.warning).register()
