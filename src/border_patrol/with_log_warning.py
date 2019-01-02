# -*- coding: utf-8 -*-
"""
Import this module to let Border-Patrol use logging with level WARNING
"""
import logging
from . import BorderPatrol

BorderPatrol(report_fun=logging.warning).register()
