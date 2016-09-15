# -*- coding: utf-8 -*-
"""Unit Tests module for `smart_query` package.
"""

__author__ = 'Papavassiliou Vassilis'


from bottle_smart_filters import SmartFiltersPlugin
import bottle


def test_plugin_setup_method_pass(mock_bottle_app):
    """Test plugin for success install.
    """

    plugin = SmartFiltersPlugin()

    mock_bottle_app.app.install(plugin)

    assert plugin in mock_bottle_app.app.plugins


def test_plugin_apply_method_pass(mock_bottle_app):
    """Test plugin for success apply method.
    """

    @mock_bottle_app.app.route('/')
    def handler():
        return {"guess": bottle.request.query.smart_filters()}

    mock_bottle_app.get('/')

    assert mock_bottle_app.get('/?id=1,2,3').json == {'guess': {'id': [1, 2, 3]}}


def test_plugin_smart_method_pass(mock_bottle_app):
    """Test plugin for success apply method.
    """

    assert mock_bottle_app.get('/?member=true').json == {'guess': {'member': True}}
    assert mock_bottle_app.get('/?member=True').json == {'guess': {'member': 'True'}}
    assert mock_bottle_app.get('/?chars=a, b, c').json == {'guess': {'chars': ['a', 'b', 'c']}}
