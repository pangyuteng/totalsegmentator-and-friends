# totalsegmentator-dataset-viewer

```
view wasserth/TotalSegmentator dataset** with rii-mongo/Papaya*
** https://github.com/rii-mango/Papaya
* https://github.com/wasserth/TotalSegmentator
```

```

# build container
docker compose build
sudo apt install mesa-utils
# prepare single segmetnation (nii.gz) file.
export DATADIR=/mnt/hd2/data/Totalsegmentator_dataset

docker run -it -u $(id -u):$(id -g) -e DATADIR --init \
    -w ${PWD} -v /mnt:/mnt totalsegmentator-dataset-viewer-flask bash

docker run -it -u $(id -u):$(id -g) -e DATADIR -e DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -w ${PWD} -v /mnt:/mnt totalsegmentator-dataset-viewer-flask bash

python prepare.py    

# update volumes in `docker-compose.yml` , and run below

docker compose up


```