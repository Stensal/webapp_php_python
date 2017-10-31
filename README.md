
## Steps to run the env

1. create the docker image
    
    ```bash
    docker image build -t stensal .
    ``` 
2. refer to the steps in "README.md" under mysql directory

3. run the docker image with phpbb
    
    *Get the full path of phpbb directory. eg., for me it is: '/var/www/webroot/stensal/webapp_php/phpbb'<br> then run this command to run the image.*
    
    ```
    docker run -it \
    -v /var/www/webroot/stensal/webapp_php/phpbb:/var/www/html/forum \
    --link forumdb:mysql \
    -p 8000:8000 stensal /bin/bash
    ```