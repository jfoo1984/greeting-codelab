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
