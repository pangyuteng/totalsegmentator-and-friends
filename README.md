# totalsegmentator-and-friends


this repo contains a few scripts used to assess/review Totalsegmentator.


#### papaya (nginx+flask) to view image and segmentation

view wasserth/TotalSegmentator dataset* with rii-mongo/Papaya**
```
* https://github.com/wasserth/TotalSegmentator
** https://github.com/rii-mango/Papaya
```
![overview](static/home.png "overview")
![view per scan with papaya](static/case.png "view per scan with papaya")

```
# tunnel `$myserver:80` as `localhost:5000`

ssh -L 5000:127.0.0.1:80 $myserver

# build container
docker compose build

# prepare single segmentation (nii.gz) file.

export DATADIR=/mnt/hd2/data/Totalsegmentator_dataset

docker run -it -u $(id -u):$(id -g) -e DATADIR --init \
    -w ${PWD} -v /mnt:/mnt totalsegmentator-dataset-viewer-flask bash

python prepare.py    

# update volumes and environment variables in `docker-compose.yml` , and run below

docker compose up

```

#### assess segementation accuracy using publically available datasets.


+ for performance assessment, see:

    + assess/ped-ct-seg/README.md

    + TODO: assess/amos2022/README.md


