PORT = 8000
HOST = '0.0.0.0'

import sys

server, appname = sys.argv[1:]

if appname == 'bottle':
    from servers.bot import app
elif appname == 'flask':
    from servers.fla import app
elif appname == 'pyramid':
    from servers.pyr import app


if __name__ == "__main__":
    if server == 'gevent':
        from gevent.wsgi import WSGIServer
        http_server = WSGIServer((HOST, PORT), app, log=None)
        http_server.serve_forever()

    elif server == 'tornado':
        from tornado.wsgi import WSGIContainer
        from tornado.httpserver import HTTPServer
        from tornado.ioloop import IOLoop

        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(PORT)
        IOLoop.instance().start()

    elif server == 'eventlet':
        from eventlet import wsgi
        import eventlet
        wsgi.server(eventlet.listen(('127.0.0.1', PORT), backlog=500), app, log=file('/dev/null', 'w'))

    elif server == 'cherrypy':
        from cherrypy import wsgiserver
        server = wsgiserver.CherryPyWSGIServer(
            (HOST, PORT), app,
            server_name='www.cherrypy.example')
        server.start()

    elif server == 'rocket':
        from rocket import Rocket
        server = Rocket((HOST, PORT), 'wsgi', {"wsgi_app":app})
        server.start()

    elif server == 'paste':
        from paste import httpserver
        httpserver.serve(app, host=HOST, port=PORT)

    elif server == 'twisted':
        from twisted.web.server import Site
        from twisted.web.wsgi import WSGIResource
        from twisted.internet import reactor

        resource = WSGIResource(reactor, reactor.getThreadPool(), app)
        reactor.listenTCP(PORT,Site(resource))
        reactor.run()


    else:
        raise Exception('wat')


