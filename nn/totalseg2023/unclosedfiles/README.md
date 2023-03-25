

docker build -t hola .
docker run -it -u $(id -u):$(id -g) -w $PWD -v $PWD:$PWD hola python hola.py