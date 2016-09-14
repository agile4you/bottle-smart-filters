# -*- coding: utf-8 -*-
#
#    Copyright (C) 2015  Papavassiliou Vassilis
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""`bottle_filters` package.

Handling Querystring Params consistent in bottle.py apps.
"""


__version__ = '0.1'

__author__ = 'Papavassiliou Vassilis'
__date__ = '2016-9-14'

__all__ = ('QueryFilterSet', 'QueryParam', 'QueryFilterError', 'QueryFilterPlugin')

from bottle_filters.parser import (QueryFilterSet, QueryParam, QueryFilterError)
import inspect
import bottle
import ujson


class QueryFilterPlugin(object):
    """A `bottle.Bottle` application plugin for JWTProvider.
    Attributes:
        keyword (str): The string keyword for application registry.
        filter_set (instance): A QueryFilterSet instance.
    """
    scope = ('plugin', 'middleware')
    api = 2

    def __init__(self, multiple_separator=','):
        self.keyword = 'query_filters'
        self.separator = multiple_separator
        self.json_identifiers = {'[', '{'}
        setattr(bottle.request.query, 'smart_query',
                lambda _: partial(self.filter_set, _))

    def setup(self, app):  # pragma: no cover
        """Make sure that other installed plugins don't affect the same
        keyword argument and check if metadata is available.
        """

        for other in app.plugins:
            if not isinstance(other, QueryFilterPlugin):
                continue
            if other.keyword == self.keyword:
                raise bottle.PluginError("Found another plugin "
                                         "with conflicting settings ("
                                         "non-unique keyword).")

    def apply(self, callback, context):  # pragma: no cover
        """Implement bottle.py API version 2 `apply` method.
        """
        from functools import partial

        def _wrapper(*args, **kwargs):
            """Decorated Injection
            """

            setattr(bottle.request, 'filter_set',
                    lambda _: self.filter_set(bottle.request.query))

            # setattr(bottle.request.query, 'smart_query',
            #          lambda _: partial(self.filter_set, _))

            return callback(*args, **kwargs)

        return _wrapper

    def filter_set(self, query_data):
        """Query Filter formatting
        """
        print(self.separator)

        request_data = dict(query_data.iteritems())

        request_filters = {}

        for alias, value in request_data.items():

            if self.separator not in value or set(value).intersection(self.json_identifiers):
                print(alias)
                try:
                    request_filters[alias] = ujson.loads(value)
                except ValueError:
                    request_filters[alias] = value
            else:

                value_list = [val.strip() for val in value.split(self.separator)]
                try:
                    request_filters[alias] = [ujson.loads(val) for val in value_list]

                except ValueError:
                    request_filters[alias] = value_list

        return request_filters
