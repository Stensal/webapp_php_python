# Portal webapp

### (1) init db

    docker-compose -f docker-compose.yml -f dockre-compose.initdb.yml up

### (2) run dev server

    docker-compose up

after containers came up, open in browser: [http://localhost](http://localhost).

## testing

### run unittests

    docker-compose -f docker-compose.tests.yml up



