


#### Some Info

*we will use these infomations in the flowing steps*

```
db_servername: forumdb
db_name: stensal_forum
db_password: 9j5H2o7epb4Y
db_port: 3306
```


#### Preparation work

1. download mysql image

    ```bash
    docker pull mysql
    ```
2. create the docker image, this step need to run in "docker" directory
    
    ```bash
    docker image build -t stensal .
    ```

3. *Get some paths on system. eg., for me the phpbb code path is: '/var/www/webroot/stensal/webapp_php/phpbb'*

    ```bash
    project_phpbb_path: /var/www/webroot/stensal/webapp_php/phpbb
    mysql_data_path: /var/www/docker/mysql/data
    ```



#### Steps to run the env

1. create a mysql server and name it as forumdb 
    ```bash
    docker run --name forumdb \
    -v /var/www/docker/mysql/data:/var/lib/mysql \
    -p 3308:3306 \
    -e MYSQL_ROOT_PASSWORD=9j5H2o7epb4Y \
    -d mysql:5.6
    ```
2. create db 'stensal_forum'
    ```bash
    mysql -h127.0.0.1 -P3308 -uroot -p9j5H2o7epb4Y
    
    create database stensal_forum default charset utf8 COLLATE utf8_general_ci;
    
    use stensal_forum;
    ```
3. import database from a db snap file under mysql/db_backups directory
    ```bash
    source /var/www/webroot/stensal/webapp_php/mysql/db_backups/stensal_forum.sql
    ```

4. run web server stensal
    ```
    docker run --name stensal_web -it \
    -v /var/www/webroot/stensal/webapp_php/docker/wwwtest:/var/www/html \
    -v /var/www/webroot/stensal/webapp_php/phpbb:/var/www/html/forum \
    --link forumdb:mysql \
    -p 8000:8000 stensal /bin/bash
    ```
5. open http://localhost:8000/forum in a browser.
    
#### FAQ
1. **get ip of mysql server**
    we can get mysql ip address by run "tail /etc/hosts" in stensal_web docker.

2. **dump a db snap**
    ```bash
    docker exec forumdb sh -c 'exec mysqldump stensal_forum -uroot -p"$MYSQL_ROOT_PASSWORD"' > ./db_backups/stensal_forum.sql
    ```
