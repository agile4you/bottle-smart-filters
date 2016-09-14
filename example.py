import bottle
from bottle.ext.filters import QueryFilterSet, QueryParam, QueryFilterError, QueryFilterPlugin


filter_specs = {
    'id': QueryParam(),
    'name': QueryParam(text=True),
    'numbers': QueryParam(multiple=True)
}

filter_set = QueryFilterSet(**filter_specs)

bottle.install(QueryFilterPlugin())


@bottle.get('/')
def index():
    import time
    time.sleep(2)
    print(hasattr(bottle.request.query, 'smart_query'))
    try:
        filters = bottle.request.filter_set()

    except QueryFilterError as error:
        return {'Error': error.args}

    return filters

if __name__ == '__main__':

    bottle.run(server='cherrypy', port=8082)
