
import sys
import cyclone.web
from twisted.python import log
from twisted.internet import reactor


class IndexHandler(cyclone.web.RequestHandler):
    def get(self):
        self.write("hello world")

class Application(cyclone.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
        ]

        cyclone.web.Application.__init__(self,
            handlers)

if __name__ == "__main__":
    #log.startLogging(sys.stdout)
    reactor.listenTCP(8000, Application())
    reactor.run()

