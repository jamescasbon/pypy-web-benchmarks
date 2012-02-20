import sys
from bottle import route, run
import bottle
from bottle_redis import RedisPlugin

app = bottle.Bottle()
plugin = RedisPlugin(host='localhost')
app.install(plugin)

if len(sys.argv) < 2:
    server = 'tornado'
else:
    server = sys.argv[1]


@app.route('/')
def stream(rdb):
    x = rdb.incr('counter')
    p = rdb.get('page')
    yield 'hello world! %s\n' % x
    yield p

run(app, host='0.0.0.0', port=8000, server=server, quiet=True)


