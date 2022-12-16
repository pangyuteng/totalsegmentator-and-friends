# totalsegmentator-dataset-viewer

```
view wasserth/TotalSegmentator dataset** with rii-mongo/Papaya*
** https://github.com/rii-mango/Papaya
* https://github.com/wasserth/TotalSegmentator
```

```

# build container
docker build -t totalsegmentator-dataset-viewer .

# prepare single segmetnation (nii.gz) file.

export DATADIR=/mnt/hd2/data/Totalsegmentator_dataset

docker run -it -u $(id -u):$(id -g) -p 5000:5000 \
    -v ${PWD}:/workdir -w /workdir \
    -v ${DATADIR}:${DATADIR} \
    -e DATADIR \
    totalsegmentator-dataset-viewer bash
python prepare.py    

# update volumes in `docker-compose.yml` , and run below

docker compose build
docker compose up


```