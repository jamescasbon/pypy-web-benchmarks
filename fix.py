import redis
import random


r = redis.StrictRedis(host='localhost', port=6379, db=0)


r.set('counter', 0)

page = ''.join([random.choice('GATC') for _ in range(2000)])

r.set('page', page)


