1.  create a docker image 
    docker image build -t t .
2.  run the docker image 
    docker run -it -p 8000:8000 t /bin/bash
3.  open http://localhost:8000 in a browser 
    run PHP test, all test should pass
4.  php code should get/set session data like unit_test.php



5. run the docker image with phpbb
Get the full path of phpbb directory. eg., for me it is: '/var/www/webroot/stensal/webapp_php/phpbb'<br> then run this command to run the image.
```
docker run -it -v [your phpbb path]:/var/www/html/forum -p 8000:8000 t /bin/bash
```