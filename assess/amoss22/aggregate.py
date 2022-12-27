#! /usr/local/bin/python
import os
import sys
import argparse
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style = 'whitegrid')

def my_plots(root_folder,output_folder,postfix=''):
    
    summary_png_file = os.path.join(output_folder,f'summary-{postfix}.png')    

    agg_csv_file = os.path.join(output_folder,f'agg-{postfix}.csv')
    summary_csv_file = os.path.join(output_folder,f'summary-{postfix}.csv')
    
    df = pd.read_csv(summary_csv_file)
    df = df.dropna() 
    df = df.reset_index()


    agg_df = pd.read_csv(agg_csv_file)
    exclude_list = ['amos_0518','amos_0517','amos_0540']
    agg_df = agg_df[agg_df.uid.apply(lambda x: x not in exclude_list)]
    mylist = []
    
    for n,row in agg_df.iterrows():
        mydict = dict(row)
        uid = mydict.pop('uid')
        for k,v in mydict.items():
            if k in ['background','prostate/uterus']:
                continue
            item = {'uid':uid,'dice':v,'organ':k}
            mylist.append(item)

    fig, axes = plt.subplots(figsize=(10,10))
    vdf = pd.DataFrame(mylist)
    sns.violinplot(vdf,x='dice',y='organ', ax = axes)
    postfix_str = f'csv basename: {os.path.basename(summary_csv_file)}, \n *3 of 360 cases excluded, modality was MR not CT.'
    plt.title(f'dice between manual vs totalsegmentator\ndataset: amos2022 (n={len(agg_df)}*), {postfix_str}')
    plt.yticks(rotation=45)
    plt.grid(True)
    plt.savefig(summary_png_file)

def main(root_folder,output_folder,postfix):
    root_folder = os.path.join(root_folder,'totalseg')

    os.makedirs(output_folder,exist_ok=True)
    
    agg_csv_file = os.path.join(output_folder,f'agg-{postfix}.csv')
    summary_csv_file = os.path.join(output_folder,f'summary-{postfix}.csv')
    

    if os.path.exists(agg_csv_file):
        raise ValueError("csv file found, please manually delete!")
    if os.path.exists(summary_csv_file):
        raise ValueError("csv file found, please manually delete!")

    json_file_list = []
    print(root_folder)
    for path in Path(root_folder).rglob("*scores.json"):
        json_file_list.append(str(path))
    case_set = set(os.listdir(root_folder))
    case_with_json_set = set([os.path.basename(os.path.dirname(x)) for x in json_file_list])

    print('cases with missing json file:',case_set-case_with_json_set)
    print(len(json_file_list))
    assert(len(json_file_list)==360)

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
    parser.add_argument('-p','--postfix',type=str,default='')
    args = parser.parse_args()
    main(args.root_folder,args.output_folder,args.postfix)
    my_plots(args.root_folder,args.output_folder,args.postfix)
"""

python aggregate.py ${root_folder} ${output_folder}

"""
