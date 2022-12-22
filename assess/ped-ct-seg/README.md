

```

ped-ct-seg
https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=89096588

download data and process dicom and segmentation to .nii.gz
https://github.com/pangyuteng/pediatric-ct-seg


python gen_args.py

condor_submit_dag condor.dag


# containers used:

https://github.com/wasserth/TotalSegmentator/blob/master/Dockerfile
docker pull wasserth/totalsegmentator_container:master

https://github.com/pangyuteng/public-scratch/tree/master/ml-docker
docker pull pangyuteng/ml:latest



```