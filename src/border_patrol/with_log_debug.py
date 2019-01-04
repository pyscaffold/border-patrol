# -*- coding: utf-8 -*-
"""
Import this module to let Border-Patrol use logging with level DEBUG
"""
from . import BorderPatrol, logger

BorderPatrol(report_fun=logger.debug).register()
