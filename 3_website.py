from bottle import get, post, request, run, template
import os

@get('/greeting')
def greeting():
    return template('3_greeting', name=None)

@post('/greeting')
def greeting_post():
    name = request.forms.get('name')
    return template('3_greeting', name=name)

run(host=os.getenv("IP"), port=os.getenv("PORT"), debug=True, reloader=True)
