# -*- coding: utf-8 -*-
"""
Import this module to let Border-Patrol use logging with level ERROR
"""
from . import BorderPatrol, logger

BorderPatrol(report_fun=logger.error).register()
