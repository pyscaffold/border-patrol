#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Dummy conftest.py for border_patrol.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    https://pytest.org/latest/plugins.html
"""

import pytest


@pytest.fixture()
def bpatrol():
    """Return BorderPatrol singleton"""
    from border_patrol import BorderPatrol

    return BorderPatrol()
