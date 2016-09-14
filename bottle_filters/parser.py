# -*- coding: utf-8 -*-
"""`bottle_filter.parser` module.

Provides main functionality for QueryString Parsing.
"""

import ujson


class QueryFilterError(Exception):
    """Base module Error.
    """
    pass


class QueryParam(object):
    """Base QueryParam class.

    The basic concept is the following: QueryParam passes ONLY text-defined parameters as is,
    and tries json-decode the others (integers, floats, booleans, JSONEncoded-string (like ES parameters etc)).

    Attributes:
        multiple (bool): Indicates if filter param accepts multiple values (default=False).
        deserialize (bool): Indicates if filter param must be deserialized (numbers, booleans, json data etc)
        separator (str): Filter value separator if filter accepts multiple values (default=',')

    Raises:
        QueryFilterError if JSONDecode Error occurs.

    Examples:
        >>> id_param = QueryParam(multiple=True)
        >>> print(id_param('1288734'))
        [1288734]
        >>> print(id_param('1288734, 8673476, 653237'))
        [1288734, 8673476, 653237]
        >>> print(id_param('Error'))
        Traceback (most recent call last):
            ...
        parser.QueryFilterError: Invalid value `Error` for <QueryParam(multiple=True, deserialize=True)>
    """
    __slots__ = ('multiple', 'deserialize', 'separator')

    def __init__(self, multiple=False, text=False, separator=','):
        self.multiple = multiple
        self.deserialize = not text
        self.separator = separator

    def parse_value(self, value):
        """Parse value according to initializing rules.
        """
        try:
            if not self.multiple:
                return ujson.loads(value) if self.deserialize else value

            value_list = [i.strip() for i in value.split(',')]
            return [ujson.loads(v) if self.deserialize else v for v in value_list]

        except ValueError:
            raise QueryFilterError('Invalid value `{}` for {}'.format(value, self))

    def __repr__(self):  # pragma: no cover
        return '<QueryParam(multiple={}, deserialize={})>'.format(
            self.multiple,
            self.deserialize
        )

    def __call__(self, value):  # pragma: no cover
        return self.parse_value(value)

    def __eq__(self, other):  # pragma: no cover
        return self.filter_name == other.filter_name

    def __hash__(self):   # pragma: no cover
        return hash(self.filter_name)

    __str__ = __repr__    # pragma: no cover


class QueryFilterSet(object):
    """Query FilterSet class.

    A container for `bottle_filter.parser.QueryParam` instances.
    Controls a collection of QueryParams and validates the collection
    against a `bottle.request.query`instance.

    Attributes:
        filters (dict): A mapping of keys, QueryParams instances.

    Examples:

        >>> filter_set = QueryFilterSet()
        >>> filter_set['age'] = QueryParam(text=False)
        >>> 'age' in filter_set
        True
        >>> from bottle import FormsDict
        >>> querystring_data = FormsDict({"age": "45"})
        >>> filter_set(querystring_data)
        {'age': 45}
        >>> del filter_set['age']
        >>> 'age' in filter_set
        False
    """
    __slots__ = ('filters', '_filter_set')

    multi_separator = ','

    def __init__(self, **query_params):  # pragma: no cover
        self.filters = query_params or dict()
        self._filter_set = set(self.filters)

    def _serialize(self, params_dict):
        """Validate a query string param mapping with contained rules.

        Args:
            params_dict (dict): A dict containing querystring data.

        Returns:
            A dict with the serialized data.

        Raises:
            QueryFilterError if request.query parameters don't match with self.filters, or
            QueryParam validation fails.
        """
        params_set = set(params_dict)

        if not params_set.issubset(self._filter_set):
            raise QueryFilterError('Invalid Filters: {}'.format(params_set.difference(self._filter_set)))

        return {k: self.filters[k](v) for k, v in params_dict.items()}

    def serialize_request(self, request_data):  # pragma: no cover
        """A proxy for `QueryFilterSet._serialize` method for using directly `bottle.request.query`
        """
        return self._serialize(dict(request_data.iteritems()))

    def __repr__(self):   # pragma: no cover
        return '<QueryFilterSet instance(Filters={})>'.format(
            self._filter_set
        )

    def __getitem__(self, item):
        """Container protocol `__getitem__` interface.
        """
        return self.filters.get(item)

    def __setitem__(self, key, value):
        """Container protocol `__setitem__`  interface.
        """
        if not isinstance(value, QueryParam):
            raise TypeError('Item must be {} instance!'.format(QueryParam))

        self.filters[key] = value
        self._filter_set.add(key)

    def __delitem__(self, key):
        """Container protocol `__delitem__` interface.
        """
        del self.filters[key]
        self._filter_set.discard(key)

    def __contains__(self, item):
        return item in self._filter_set

    def __call__(self, request_data):  # pragma: no cover
        """Proxy `QueryFilterSet.serialize_request` method.
        """
        return self.serialize_request(request_data)

    __str__ = __repr__
