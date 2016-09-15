# -*- coding: utf-8 -*-
"""Unit test suite for `bottle_smart_filters` project.
"""

__author__ = 'Papavassiliou Vassilis'
__date__ = '2016-9-14'


import pytest
import webtest
import bottle
from bottle_smart_filters import SmartFiltersPlugin


@pytest.fixture(scope='session')
def mock_bottle_app():
    """pytest fixture for `bottle.Bottle` instance.
    """
    return webtest.TestApp(bottle.Bottle())
