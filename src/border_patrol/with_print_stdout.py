# -*- coding: utf-8 -*-
"""
Import this module to let Border-Patrol use plain print
"""
from . import BorderPatrol

BorderPatrol(report_fun=print).register()
