# -*- coding: utf-8 -*-
"""
Import this module to let Border-Patrol use plain print on stderr
"""
import sys

from . import BorderPatrol

BorderPatrol(report_fun=lambda x: print(x, file=sys.stderr)).register()
