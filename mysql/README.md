## Steps to run the mysql server

#### Some Info
*we will use these infomations in the flowing steps*
```
db_servername: forumdb
db_name: stensal_forum
db_password: 9j5H2o7epb4Y
db_port: 3306
project_mysql_dir: /var/www/webroot/stensal/webapp_php/mysql
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

#### Two methods to manage the mysql server
1. use mysql client on host machine 
    ```bash
    mysql -h127.0.0.1 -P3308 -uroot -p9j5H2o7epb4Y
    ```
2. use docker 
    ```bash
    docker run -it --link forumdb:mysql \
    --rm mysql:5.6 \
    sh -c 'exec mysql -h"$MYSQL_PORT_3306_TCP_ADDR" -P"$MYSQL_PORT_3306_TCP_PORT" -uroot -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD"'
    ```
#### Export the db snap
```bash
docker exec forumdb sh -c 'exec mysqldump stensal_forum -uroot -p"$MYSQL_ROOT_PASSWORD"' > ./db_backups/stensal_forum.sql
```