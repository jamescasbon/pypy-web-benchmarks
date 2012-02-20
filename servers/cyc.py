import sys
import cyclone.web
import cyclone.redis
from twisted.python import log
from twisted.internet import reactor
from twisted.internet import defer

class IndexHandler(cyclone.web.RequestHandler):

    @defer.inlineCallbacks
    def get(self):
        db = self.settings.db
        x = yield db.incr('counter')
        self.write("hello world %s\n"  % x)
        p = yield db.get('page')
        self.write(p)


class Application(cyclone.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
        ]
        settings = dict(
            db = cyclone.redis.lazyConnectionPool("127.0.0.1", 6379,0, 10)
        )

        cyclone.web.Application.__init__(self,
            handlers, **settings)

if __name__ == "__main__":
    #log.startLogging(sys.stdout)
    reactor.listenTCP(8000, Application())
    reactor.run()

