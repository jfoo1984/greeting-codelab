# Greetings Codelab

In this codelab you will make a greeting generator that makes use of the following technologies:

 * Cloud 9
 * Python-based web server (bottle.py)
 * HTML and CSS
 * Server-side persistent storage (Redis)

The source code for the lessons are available [on GitHub](https://github.com/jeztek/greeting-codelab).

## Lesson 1 - bottle.py

This should look familiar:

```python
def greeting(name):
	print "Hi %s, pleased to meet you!" % (name)
   
>>> greeting("Sarah")
Hi Sarah, pleased to meet you!
```

Let's try to do the same thing but as a website using bottle.py. First, create a Cloud 9 workspace called greeting.  Then in a terminal, run the following command to make sure to install  bottle.py:

```bash
sudo pip install bottle
```

Save the following code as ```website.py```:
```python
from bottle import route, run, template

@route('/greeting/<name>')
def greeting(name):
	return template("Hi {{name}}, pleased to meet you!", name=name)
    
run(host=os.getenv("IP"), port=os.getenv("PORT"), debug=True, reloader=True)
```

Hit run.   You should be able to access the website here:

```
https://greeting-<username>.c9.io/greeting/<name>
```

Make sure to substitute ```username``` and ```name``` with your own values.

What's going on here?

 * bottle.py methods: route, run, template
 * Web browser URL parsing
 * Browser, HTTP, DNS, TCP/IP, routers, web server
 
## Lesson 2 - HTTP Request

This is great if we already know your name, but what if we want to ask you for it?

Web servers respond to several types of HTTP requests:

 * GET
 * POST
 * PUT
 * DELETE

In lesson 1 we made a GET request to fetch data, but it's customary to send data back via POST.  In ```website.py```, update your import statements and replace your greeting function with the following two new functions:

```python
from bottle import get, post, request, run, template

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
```

We now have two seperate handlers, one to return some HTML via GET, and one to accept the form response via POST.

## Lesson 3 - HTML and templates

This is all great, but I don't want to mix my python and HTML code.  Let's seperate the two by moving the HTML code to a template.  Modify your two functions so they look like this:

```python
@get('/greeting')
def greeting():
    return template('greeting', name=None)

@post('/greeting')
def greeting_post():
    name = request.forms.get('name')
    return template('greeting', name=name)
```

and create a new folder called ```views``` and create a new file called ```greeting.tpl``` inside with the following contents:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>The Greeting Generator</title>
  </head>
  
  <body>
    % if name:
    <div>
      Hi {{name}}, pleased to meet you!
    </div>
    <div>
      <a href="/greeting">Start over</a>
    </div>
    % else:
    <div>
      <div>Hi what's your name?</div>
      <form action="/greeting" method="post">
        <input name="name" type="text" />
        <input value="Submit" type="submit" />
      </form>
    </div>
    % end
  </body>
</html>
```

What's going on here?

 * separate HTML file
 * HTML tags: head, body, div, form, input
 * bottle.py templating language

## Lesson 4 - CSS

How do I make my site look prettier?  Modify ```greeting.tpl``` so it looks like the code below.  Note the addition of the ```<style>``` tag within ```<head>``` and the addition of ```id=``` fields for a few of the ```div```'s.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>The Greeting Generator</title>
    <style>
      body {
        font-family: Arial;
        font-size: 11pt;
        margin: 10px;
      }
      #prompt {
        margin-bottom: 10px;
      }
      #greeting {
        margin-bottom: 10px;
      }
    </style>
  </head>
  
  <body>
    % if name:
    <div id="greeting">
      Hi {{name}}, pleased to meet you!
    </div>
    <div>
      <a href="/greeting">Start over</a>
    </div>
    % else:
    <div id="form">
      <div id="prompt">Hi what's your name?</div>
      <form action="/greeting" method="post">
        <input name="name" type="text" />
        <input value="Submit" type="submit" />
      </form>
    </div>
    % end
  </body>
</html>

```

What's going on here?

 * CSS styling that references tags in HTML
 * CSS styling can be referenced via HTML element name, id, or class
 * Try inspecting elements in the browser

## Lesson 5 - Data persistence using Redis

How do I store data?  Let's use [Redis](http://redis.io/) to store some data.

In a terminal, run the following commands to start Redis and install Python bindings for Redis:

```bash
sudo service redis-server start
sudo pip install redis
```

Next, modify ```website.py``` so it looks like the code below.  Note the additional Redis references:

```python
import redis
r = redis.Redis()

@get('/greeting')
def greeting():
    summary = r.hgetall('names')
    return template('greeting', name=None, summary=summary)

@post('/greeting')
def greeting_post():
    name = request.forms.get('name')
    r.hincrby('names', name, 1)
    return template('greeting', name=name, summary=None)
```

and modify ```greeting.tpl``` to match the code below.  The only addition is the ```table``` inside the ```%else``` block.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>The Greeting Generator</title>
    <style>
      body {
        font-family: Arial;
        font-size: 11pt;
        margin: 10px;
      }
      table {
        margin-top: 10px;
      }
      table td {
        padding: 0px 10px 0px 0px;
      }
      #prompt {
        margin-bottom: 10px;
      }
      #greeting {
        margin-bottom: 10px;
      }
    </style>
  </head>
  
  <body>
    % if name:
    <div id="greeting">
      Hi {{name}}, pleased to meet you!
    </div>
    <div>
      <a href="/greeting">Start over</a>
    </div>
    % else:
    <div id="form">
      <div id="prompt">Hi what's your name?</div>
      <form action="/greeting" method="post">
        <input name="name" type="text" />
        <input value="Submit" type="submit" />
      </form>
    </div>

    <table>
      <tr>
        <td>Name</td>
        <td>Count</td>
      </tr>
    % for name in summary.keys():
      <tr>
        <td>{{name}}</td>
        <td>{{summary[name]}}</td>
      </tr>
    % end
    </table>
    % end
  </body>
</html>
```

What's going on here?

 * Redis hash data structure to count instances of each name
 * Render contents of hash table in HTML on GET request
 * Data is persisted in Redis
