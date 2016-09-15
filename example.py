import bottle
from bottle.ext.smart_filters import SmartFiltersPlugin

bottle.install(SmartFiltersPlugin())


@bottle.get('/')
def index():
    return {'smart_filters': bottle.request.query.smart_filters()}

if __name__ == '__main__':
    bottle.run()
