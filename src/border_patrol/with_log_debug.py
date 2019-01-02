# -*- coding: utf-8 -*-
"""
Import this module to let Border-Patrol use logging with level DEBUG
"""
import logging
from . import BorderPatrol

BorderPatrol(report_fun=logging.debug).register()
