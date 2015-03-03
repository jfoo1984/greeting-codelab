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
    <div>
      <div id="prompt">Hi what's your name?</div>
      <form action="/greeting" method="post">
        <input name="name" type="text" />
        <input value="Submit" type="submit" />
      </form>
    </div>
    % end
  </body>
</html>
