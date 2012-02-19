from gevent import wsgi

class WebServer(object):
    def application(self, environ, start_response):
        start_response("200 OK", [])
        return ["Hello world!"]

if __name__ == "__main__":
    app = WebServer()
    wsgi.WSGIServer(('', 8000), app.application, backlog=1024, log=None).serve_forever()

