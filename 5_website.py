from bottle import get, post, request, run, template
import os
import redis

r = redis.Redis()

@get('/greeting')
def greeting():
    summary = r.hgetall('names')
    return template('5_greeting', name=None, summary=summary)

@post('/greeting')
def greeting_post():
    name = request.forms.get('name')
    r.hincrby('names', name, 1)
    return template('4_greeting', name=name, summary=None)

run(host=os.getenv("IP"), port=os.getenv("PORT"), debug=True, reloader=True)
