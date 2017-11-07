## Install environment
1. install docker compose first
2. run below command to start all services (in the directory where "docker-compose.yml" file exists)
    ```
    docker-compose up -d
    ```
3. for more detail please refer the usage of docker compose




## How to test forum with github login
1. Add an "github-auth-config.php" under "wwwtest" directory, set your github auth app configurations here:
for example:
```php
define('OAUTH2_CLIENT_ID', '*******');
define('OAUTH2_CLIENT_SECRET', '********');
define('HOME_URI', 'http://localhost:8000/auth.php');
define('REDIRECT_URI', 'http://localhost:8000/auth.php?callback');
```

2. Open "http://localhost:8000/auth.php" on a browser and click on login, you should be able to see the results which contains
the github user info. 

3. Open "http://localhost:8000/forum/" and see if you are already logged in.