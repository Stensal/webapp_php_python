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