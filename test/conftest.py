# -*- coding: utf-8 -*-
"""Unit test suite for `bottle_filters` project.
"""

__author__ = 'Papavassiliou Vassilis'
__date__ = '2016-9-14'


import pytest
from bottle import FormsDict


@pytest.fixture(scope='session')
def mock_request_params():
    """pytest fixture for `bottle.request.query` instance.
    """

    request_dict = {
        'id': '176732',
        'name': 'DevTeam',
        'active': 'true',
        'tags': 'python, Postgresql, bottle.py, web'
    }

    return FormsDict(request_dict)
