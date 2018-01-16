# Portal webapp

### For the first time execution of the webapp

    docker-compose -f docker-compose.yml -f docker-compose.initdb.yml up


### For the subsequent executions of the webapp

    docker-compose up 

after containers came up, open in browser: [http://localhost](http://localhost).

## testing

### run tests

(1) start containers

    docker-compose -f docker-compose.tests.yml up -d

(2) run tests:

    docker exec -ti portal_web_tests python /data/app/tests/test_main.py -c tests


