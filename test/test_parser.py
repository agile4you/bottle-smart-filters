# -*- coding: utf-8 -*-
"""Unit Tests module for `bottle_filters.parser` module.
"""

__author__ = 'Papavassiliou Vassilis'


import pytest
from bottle_filters.parser import (
    QueryParam, QueryFilterError, QueryFilterSet
)


def test_query_param_text_pass():
    """Test QueryParam for str parameter.
    """

    text_param = QueryParam(text=True)

    assert text_param('pass_through') == 'pass_through'


def test_query_param_int_pass():
    """Test QueryParam for int parameter.
    """
    int_param = QueryParam()

    assert int_param('10') == 10


def test_query_param_float_pass():
    """Test QueryParam for float parameter.
    """
    float_param = QueryParam()

    assert float_param('10.001') == 10.001


def test_query_param_boolean_pass():
    """Test QueryParam for bool parameter.
    """
    bool_param = QueryParam()

    assert bool_param('true') is True


def test_query_multiple_param_pass():
    """Test QueryParam for bool parameter.
    """
    int_param = QueryParam(multiple=True)

    assert int_param('1, 2, 3, 19') == [1, 2, 3, 19]


def test_query_param_fail():
    """Test QueryParam for parameter validation failure.
    """
    int_param = QueryParam()

    with pytest.raises(QueryFilterError):
        int_param('123abc')


def test_query_set_filter_magic_methods():
    """Test QueryFilterSet data model.
    """
    query_filter_set = QueryFilterSet()

    query_filter_set['id'] = QueryParam()

    assert 'id' in query_filter_set
    assert isinstance(query_filter_set['id'], QueryParam)

    del query_filter_set['id']

    assert 'id' not in query_filter_set


def test_query_set_filter_serialize_pass(mock_request_params):
    """Test QueryFilterSet.serialize method pass.
    """
    filter_set = QueryFilterSet()

    filter_set['id'] = QueryParam()
    filter_set['name'] = QueryParam(text=True)
    filter_set['active'] = QueryParam()
    filter_set['tags'] = QueryParam(text=True, multiple=True)

    expected_data = {
        'id': 176732,
        'name': 'DevTeam',
        'active': True,
        'tags': ['python', 'Postgresql', 'bottle.py', 'web']
    }

    assert expected_data == filter_set(mock_request_params)


def test_query_set_filter_serialize_fail(mock_request_params):
    """Test QueryFilterSet.serialize method fail.
    """
    filter_set = QueryFilterSet()

    filter_set['id'] = QueryParam()
    filter_set['name'] = QueryParam(text=True)
    filter_set['active'] = QueryParam()

    with pytest.raises(QueryFilterError):
        filter_set(mock_request_params)
