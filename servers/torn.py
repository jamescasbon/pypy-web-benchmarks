import tornado.ioloop
import tornado.web
import redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        r = redis.Redis(connection_pool=pool)
        x = r.incr('counter')
        self.write("Hello, world %s\n" % x)
        self.write(r.get('page'))

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
