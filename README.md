


#### Some Info

*we will use these infomations in the flowing steps*
```
db_servername: forumdb
db_name: stensal_forum
db_password: 9j5H2o7epb4Y
db_port: 3306
```

*Get some path of your project. eg., for me the phpbb path is: '/var/www/webroot/stensal/webapp_php/phpbb'*
```
project_mysql_path: /var/www/webroot/stensal/webapp_php/mysql
project_phpbb_path: /var/www/webroot/stensal/webapp_php/phpbb
```

#### run mysql server
1. download mysql image

    ```bash
    docker pull mysql
    ```
2. create a mysql server and name it as forumdb 
    ```bash
    docker run --name forumdb \
    -v /var/www/webroot/stensal/webapp_php/mysql/data:/var/lib/mysql \
    -p 3308:3306 \
    -e MYSQL_ROOT_PASSWORD=9j5H2o7epb4Y \
    -d mysql:5.6
    ```


#### Steps to run the env

*please run mysql server first before doing this step*

1. create the docker image, this step need to run in "docker" directory
    
    ```bash
    docker image build -t stensal .
    ``` 
2. run the docker image with phpbb
    
    ```
    docker run --name stensal_web -it \
    -v /var/www/webroot/stensal/webapp_php/phpbb:/var/www/html/forum \
    --link forumdb:mysql \
    -p 8000:8000 stensal /bin/bash
    ```
    
    
    
#### FAQ
1. **get ip of mysql server**
    we can get mysql ip address by run "tail /etc/hosts" in stensal_web docker.
2. 
