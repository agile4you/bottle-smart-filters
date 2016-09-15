**bottle-smart-filters**:  *Bottle Querystring smart guessing*

Provides a bottle.py plugin for querystring parameters smart guessing.

Features:
---------
    - Provides default type casting for integers, floats, booleans.
    - Provides a mechanism for multiple value params through separators.
    - Smart filter is attached to `bottle.Bottle.request.query` instance,
      so it doesn't mess your implementation.
    - Useful Pre-processor for any validation library or custom implementation.


.. note:: This is NOT A Querystring validation library!

.. image:: https://travis-ci.org/agile4you/bottle-jwt.svg?branch=master
    :target: https://travis-ci.org/agile4you/bottle-smart-filters

.. image:: https://coveralls.io/repos/agile4you/bottle-jwt/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/agile4you/bottle-smart-filters?branch=master

*Example Usage*

.. code:: python

    import bottle
    from bottle.ext.smart_filters import SmartFiltersPlugin

    bottle.install(SmartFiltersPlugin())

    @bottle.get('/')
    def index():
        return {'smart_filters': bottle.request.query.smart_filters()}


    bottle.run()


*Example endpoints*::

    - GET /?id=12434&membership=true&score=9.4&email=someone@somewhere.com
        * Smart Filter output:
          {"id": 12343, "member": True, "score": 9.4, "email": "someone@somewhere.com"}

    - GET /?numbers=1,2, 3,4,5
        * Smart Filter output:
          {"number": [1, 2, 3, 4, 5]}
