# totalsegmentator-dataset-viewer


```
docker build -t totalsegmentator-dataset-viewer .

export DATADIR=/mnt/hd2/data/Totalsegmentator_dataset/

docker run -it -u $(id -u):$(id -g) -p 5000:5000 \
    -v ${PWD}:/workdir -w /workdir \
    -v ${DATADIR}:/mnt/Totalsegmentator_dataset \
    -e DATADIR=/mnt/Totalsegmentator_dataset\
    totalsegmentator-dataset-viewer bash

```