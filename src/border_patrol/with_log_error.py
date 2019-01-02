import logging
from . import BorderPatrol

BorderPatrol(report_fun=logging.error).register()
