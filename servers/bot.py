from gevent import monkey; monkey.patch_all()

from bottle import route, run

@route('/')
def stream():
    return 'hello world!'

run(host='0.0.0.0', port=8000, server='gevent', quiet=True)


