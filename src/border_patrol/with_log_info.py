# -*- coding: utf-8 -*-
"""
Import this module to let Border-Patrol use logging with level INFO
"""
import logging
from . import BorderPatrol

BorderPatrol(report_fun=logging.info).register()
