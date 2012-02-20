import sys
from flask import Flask
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import redis

app = Flask(__name__)


redisdb = redis.ConnectionPool(host='localhost')


@app.route("/")
def hello():
    db = redis.Redis(connection_pool=redisdb)
    x = db.incr('counter')
    p = db.get('page')
    return "Hello World! %s\n%s" % (x, p)



if len(sys.argv) < 2:
    server = 'tornado'
else:
    server = sys.argv[1]


if __name__ == "__main__":
    if server == 'gevent':
        from gevent.wsgi import WSGIServer
        http_server = WSGIServer(('', 8000), app, log=None)
        http_server.serve_forever()

    elif server == 'tornado':
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(8000)
        IOLoop.instance().start()
    else:
        raise Exception('wat')
