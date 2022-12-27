
# instructions

```

# download amos

#inside docker
docker run -it -u $(id -u):$(id -g) \
    -w $PWD -v /mnt:/mnt pangyuteng/ml:latest bash
python gen_args.py /mnt/scratch/data/amos22 results

#outside docker
condor_subit_dag condor_dag

```

# results

Dice computed between manual contours and TotalSegmentor predictions using dataset AMOS2022 (n=357*)

![png](results/summary-default.png "png")
* 3 of 360 cases excluded, modality was MR not CT