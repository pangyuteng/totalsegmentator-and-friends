

## data
```
ped-ct-seg
https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=89096588

```

## notes
```
+ download data and process dicom and segmentation to .nii.gz
https://github.com/pangyuteng/pediatric-ct-seg

+ run below to generate *.args
python gen_args.py $DATADIR

+ submit inference and dice computation jobs.
condor_submit_dag condor.dag

+ run below to generate agg.csv and summary.csv
python aggregate.py $DATADIR

```

## containers used in condor jobs
```
https://github.com/wasserth/TotalSegmentator/blob/master/Dockerfile
docker pull wasserth/totalsegmentator_container:master

https://github.com/pangyuteng/public-scratch/tree/master/ml-docker
docker pull pangyuteng/ml:latest

```
