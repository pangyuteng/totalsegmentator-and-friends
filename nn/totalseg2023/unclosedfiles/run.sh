#!/bin/bash

docker build -t notworking -f Dockerfile.notworking .
docker run -it -u $(id -u):$(id -g) -w $PWD -v $PWD:$PWD notworking python hola.py

docker build -t working -f Dockerfile.working .
docker run -it -u $(id -u):$(id -g) -w $PWD -v $PWD:$PWD working python hola.py

