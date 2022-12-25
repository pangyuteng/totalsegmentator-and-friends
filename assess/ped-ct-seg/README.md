

## dataset

dataset ped-ct-seg
https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=89096588

## notes

+ download data and process dicom and segmentation to .nii.gz
https://github.com/pangyuteng/pediatric-ct-seg

+ run below to generate *.args
python gen_args.py $DATADIR $RESULTSDIR

+ submit inference and dice computation, and results aggregation DAG jobs.
rm condor.dag.* docker_stderror log/* results/*.csv
condor_submit_dag condor.dag

```

## containers used in condor jobs

https://github.com/wasserth/TotalSegmentator/blob/master/Dockerfile
https://github.com/pangyuteng/totalsegmentator-and-friends/blob/main/assess/docker-with-weights/Dockerfile
``` # contains model weights as one layer
docker pull pangyuteng/totalsegmentator:latest
```

https://github.com/pangyuteng/public-scratch/tree/master/ml-docker
```
docker pull pangyuteng/ml:latest
```
