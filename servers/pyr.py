from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

from gevent.wsgi import WSGIServer

def hello_world(request):
   return Response('Hello world!')


if __name__ == '__main__':
    config = Configurator()
    config.add_view(hello_world)
    app = config.make_wsgi_app()

    #server = make_server('0.0.0.0', 8000, app)
    #server.serve_forever()

    http_server = WSGIServer(('', 8000), app, log=None)
    http_server.serve_forever()
