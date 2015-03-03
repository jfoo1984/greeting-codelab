# Greeting Generator Codelab

In this codelab you will make a greeting generator that makes use of the following technologies:

 * [Cloud 9](https://c9.io/)
 * Python-based web server ([bottle.py](http://bottlepy.org/))
 * HTML and CSS
 * Server-side persistent storage ([Redis](http://redis.io/))

The source code for the lessons are available [on GitHub](https://github.com/jeztek/greeting-codelab).

## Lesson 1 - bottle.py

This should look familiar:

```python
def greeting(name):
	print "Hi %s, pleased to meet you!" % (name)

>>> greeting("Sarah")
Hi Sarah, pleased to meet you!
```

Let's try to do the same thing but as a website using bottle.py. First, create a Cloud 9 workspace called greeting. Then in a terminal, run the following command to install bottle.py:

```bash
sudo pip install bottle
```

Save the following code as `website.py`:
```python
from bottle import route, run, template
import os

@route('/greeting/<name>')
def greeting(name):
	return template("Hi {{name}}, pleased to meet you!", name=name)

run(host=os.getenv("IP"), port=os.getenv("PORT"), debug=True, reloader=True)
```

Hit run. You should be able to access the website here:

```
https://greeting-<username>.c9.io/greeting/<name>
```

Make sure to substitute `<username>` and `<name>` with your own values.

#### What's going on?

 * bottle.py methods: route, run, template
 * Web browser URL parsing
 * Browser, HTTP, DNS, TCP/IP, routers, web server

#### Learn more
 * [W3 article on "How does the Internet work?"](http://www.w3.org/wiki/How_does_the_Internet_work).
 * [bottle.py tutorial](http://bottlepy.org/docs/dev/tutorial.html)

## Lesson 2 - HTTP Request

This is great if we already know your name, but what if we want to ask you for it?

Web servers respond to several types of HTTP requests but the most popular are:

 * GET
 * POST

In lesson 1 we made a GET request to fetch data, but it's customary to send data back via POST.  In `website.py`, update your import statements and replace your greeting function with the following two new functions:

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

Perform a GET request by opening the following URL:
```
https://greeting-<username>.c9.io/greeting
```

#### What's going on?

 * Seperate handlers for GET and POST requests
   * GET to fetch HTML page
   * POST to receive form response
 * HTML form
 * New bottle.py methods: get, post, request

#### Learn more

 * [Wikipedia article on HTTP request methods](http://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods)
 * [HTML form tag documentation](http://www.w3schools.com/tags/tag_form.asp)

## Lesson 3 - HTML and templates

This is all great, but I don't want to mix my python and HTML code. Mixing the two makes it hard to read, especially when there's lots of HTML.

Let's seperate our Python and HTML code by moving the HTML code into a template file.  First, modify your two request handler functions so they look like this:

```python
@get('/greeting')
def greeting():
    return template('greeting', name=None)

@post('/greeting')
def greeting_post():
    name = request.forms.get('name')
    return template('greeting', name=name)
```

Next, create a new folder called `views` and create a new file called ```greeting.l` inside it with the following contents:

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

#### What's going on?

 * separate HTML file
 * First parameter to `template()` function is name of `.tpl` file to render
 * bottle.py templating language: `%`, `{{ }}`
 * HTML tags: head, body, div, form, input

#### Learn more

 * [HTML tags reference](http://www.w3schools.com/tags/)
 * [bottle.py SimpleTemplate Engine documentation](http://bottlepy.org/docs/dev/stpl.html)
 * Try viewing the source of your favorite website

## Lesson 4 - CSS

My site looks ugly. How do I make it look prettier?

CSS, or cascading style sheets, is a language used to specify the look and formatting of a document. It's used to seperate a document's content from it's presentation.

Modify `greeting.tpl` so it looks like the code below.  Note the addition of the `<style>` tag within `<head>` and the addition of `id=` fields for a few of the `<div>`'s.

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

#### What's going on?

 * CSS selectors reference tag properties in HTML
 * CSS selectors refer to HTML tag name, id, or class

#### Learn more

 * [Wikipedia article about CSS](http://en.wikipedia.org/wiki/Cascading_Style_Sheets)
 * Try inspecting elements in the browser and modify their CSS properties
 
## Lesson 5 - Data persistence using Redis

I'd like to store the names my users submit. How can I do this?

Let's use [Redis](http://redis.io/) for server-side data persistence. Redis is a very popular in-memory data structure storage server.

In particular, let's store each name in a dictionary and keep track of how many times we've seen teach name.

In a terminal, run the following commands to start the Redis server and install Python bindings for Redis:

```bash
sudo service redis-server start
sudo pip install redis
```

Next, modify `website.py` so it looks like the code below.  Note the additional Redis references, `r.hgetall()` and `r.hincrby()`, and new variable `summary` passed into `template()`:

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

Finally, modify `greeting.tpl` to match the code below.  The only addition is the `table` inside the `%else` block.

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

#### What's going on?

 * Redis dictionary (hash) data structure to count instances of each name
 * Redis commands `HGETALL` and `HINCRBY`
 * Render contents of hash table in HTML on GET request

#### Learn more

 * [Redis command reference](http://redis.io/commands)
 * Experiment with Redis commands using `redis-cli`
