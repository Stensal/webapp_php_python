1.  create a docker image 
    docker image build -t t .
2.  run the docker image 
    docker run -it -p 8000:8000 t /bin/bash
3.  open http://localhost:8000 in a browser 
    run PHP test, all test should pass
