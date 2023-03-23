

`totalseg2023` - idea is to pretrain with totalsegmentator dataset and
then use the weights to train again for better lungseg in folder `lungseg2023`

docker run -it -u $(id -u):$(id -g) -w $PWD -v /radraid:/radraid -v /cvibraid:/cvibraid -v /scratch2:/scratch2 registry.cvib.ucla.edu/pteng:lungseg2023 bash