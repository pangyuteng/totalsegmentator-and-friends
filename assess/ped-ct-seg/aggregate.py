import os
import sys
from pathlib import Path
import json
import numpy as np
import pandas as pd

agg_csv_file = 'agg.csv'
summary_csv_file = 'summary.csv'
def main(root_folder):

    if not os.path.exists(agg_csv_file):
        json_file_list = []
        for path in Path(root_folder).rglob("*scores.json"):
            json_file_list.append(str(path))

        mylist = []
        for x in json_file_list:
            uid = os.path.basename(os.path.dirname(x))
            with open(x,'r') as f:
                scores_dict = json.loads(f.read())
            myitem = scores_dict['dice']
            myitem['uid']=uid
            mylist.append(myitem)

        df = pd.DataFrame(mylist)
        df.to_csv(agg_csv_file,index=False)
    else:
        df = pd.read_csv(agg_csv_file)

    if not os.path.exists(summary_csv_file):
        mylist = []
        for organ_name in df.columns:
            if organ_name == "uid":
                continue
            myitem=dict(
                organ_name=organ_name,
            )
            val_list = df[organ_name].dropna()
            if len(val_list)>0:
                n = len(val_list)
                m,sd = np.mean(val_list),np.std(val_list)
                med = np.median(val_list)
                myitem.update(dict(
                    val_median=np.round(med,4),
                    val_mean=np.round(m,4),
                    val_sd=np.round(sd,4),
                    val_n=n,
                ))
            mylist.append(myitem)
        df = pd.DataFrame(mylist)
        df.to_csv(summary_csv_file,index=False)

    dtype_dict = {'val_median':'Float32','val_mean':"Float32",'val_sd':"Float32",'val_n':"Int64"}
    df = pd.read_csv(summary_csv_file,dtype=dtype_dict)
    print(df)


if __name__ == "__main__":
    root_folder = sys.argv[1]
    main(root_folder)

"""
docker run -it -u $(id -u):$(id -g) \
    -w $PWD -v /cvibraid:/cvibraid -v /radraid:/radraid \
    pangyuteng/ml:latest bash

python aggregate.py /radraid/pteng/ped-ct-seg-nifti
"""
