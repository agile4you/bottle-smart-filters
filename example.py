from gevent import monkey
monkey.patch_all()

import bottle
from bottle.ext.filters import SmartFiltersPlugin


bottle.install(SmartFiltersPlugin())


@bottle.get('/')
def index():
    print(bottle.request.query.smart_query())
    return {'smart_filters': bottle.request.query.smart_filters()}

if __name__ == '__main__':
    bottle.run(server='gevent', port=8082)
