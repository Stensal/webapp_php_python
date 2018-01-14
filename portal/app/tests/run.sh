#!/bin/bash

docker exec -ti portal_web_tests python /data/app/tests/test_main.py -c tests
