from bottle import get, post, request, run, template
import os

@get('/greeting')
def greeting():
    return '''
        <form action="/greeting" method="post">
            <input name="name" type="text" />
            <input value="Submit" type="submit" />
        </form>
    '''
@post('/greeting')
def greeting_post():
    name = request.forms.get('name')
    return template('Hi {{name}}, pleased to meet you!', name=name)

    
run(host=os.getenv("IP"), port=os.getenv("PORT"), debug=True, reloader=True)
