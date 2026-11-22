import redis
import time
from flask import Flask, make_response
import socket

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count() -> int:
    retries = 5
    while True:
        try: return int(cache.get('hits') or 0)
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
              raise exc
            retries -=1
            time.sleep(0.5)

def incr_hit_count() -> int:
    return cache.incr('hits')

@app.route('/')
def hello():
    incr_hit_count()
    count = get_hit_count()
    return 'Hello World VERSION 5! I have been seen {} times. My name is: {}\n'.format(count, socket.gethostname())
