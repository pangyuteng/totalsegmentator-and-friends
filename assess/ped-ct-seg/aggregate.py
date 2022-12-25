#! /usr/local/bin/python
import os
import sys
import argparse
from pathlib import Path
import json
import numpy as np
import pandas as pd

def main(root_folder,output_folder):

    os.makedirs(output_folder,exist_ok=True)
    
    agg_csv_file = os.path.join(output_folder,'agg.csv')
    summary_csv_file = os.path.join(output_folder,'summary.csv')

    if os.path.exists(agg_csv_file):
        raise ValueError("csv file found, please manually delete!")
    if os.path.exists(summary_csv_file):
        raise ValueError("csv file found, please manually delete!")

    json_file_list = []
    print(root_folder)
    for path in Path(root_folder).rglob("*scores.json"):
        json_file_list.append(str(path))
    print(json_file_list,'!!!!')
    mylist = []
    for x in json_file_list:
        uid = os.path.basename(os.path.dirname(x))
        with open(x,'r') as f:
            scores_dict = json.loads(f.read())

        myitem={'uid':uid}
        myitem.update(scores_dict['dice'])
        mylist.append(myitem)

    agg_df = pd.DataFrame(mylist)
    agg_df.to_csv(agg_csv_file,index=False)

    sample_n = len(agg_df)

    mylist = []
    for organ_name in agg_df.columns:
        if organ_name == "uid":
            continue
        myitem=dict(
            organ_name=organ_name,
        )
        val_list = agg_df[organ_name].dropna()
        if len(val_list)>0:
            n = len(val_list)
            m,sd = np.mean(val_list),np.std(val_list)
            med = np.median(val_list)
            myitem.update(dict(
                dice_median=np.round(med,4),
                dice_mean=np.round(m,4),
                dice_sd=np.round(sd,4),
                n=n,
            ))
        mylist.append(myitem)
    df = pd.DataFrame(mylist)
    df.to_csv(summary_csv_file,index=False)

    dtype_dict = {'dice_median':'Float32','dice_mean':"Float32",'dice_sd':"Float32",'n':"Int64"}
    df = pd.read_csv(summary_csv_file,dtype=dtype_dict)
    df = df.dropna()
    print(f'dice score of organs predicted TotalSegmentator(dataset: ped-ct-org, n={sample_n})')
    print(df)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('root_folder',type=str)
    parser.add_argument('output_folder',type=str)
    args = parser.parse_args()
    main(args.root_folder,args.output_folder)

"""

python aggregate.py ${root_folder} ${output_folder}

"""
