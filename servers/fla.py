from flask import Flask
app = Flask(__name__)
from gevent.wsgi import WSGIServer

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    #     app.run(port=8000)

    http_server = WSGIServer(('', 8000), app, log=None)
    http_server.serve_forever()
