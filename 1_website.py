from bottle import route, run, template
import os

@route('/greeting/<name>')
def greeting(name):
    return template("Hi {{name}}, pleased to meet you!", name=name)

run(host=os.getenv("IP"), port=os.getenv("PORT"), debug=True, reloader=True)
