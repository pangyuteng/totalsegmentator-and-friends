#! /usr/local/bin/python
import os
import sys
import argparse
from pathlib import Path
import json
import numpy as np
import pandas as pd
from tqdm import tqdm
import pydicom
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style = 'whitegrid')

def compare_results():
    default_df = pd.read_csv('results/agg-default.csv')
    fast_df = pd.read_csv('results/agg-fast.csv')

    mylist = []
    for uid in default_df.uid.unique():

        defaut_item = default_df[default_df.uid==uid].iloc[0,:]
        fast_item = fast_df[fast_df.uid==uid].iloc[0,:]
        organ_list = sorted([x for x in defaut_item.keys() if x != 'uid'])

        for organ_name in organ_list:

            if np.isnan(defaut_item[organ_name]) or np.isnan(fast_item[organ_name]):
                continue

            for kind,kind_int,item_dict in [
                ('default',0,defaut_item),
                ('fast',1,fast_item)]:

                myitem = dict(uid=uid)
                myitem['organ']=organ_name
                myitem['kind']=kind
                myitem['kind_int']=kind_int
                myitem['dice']=item_dict[organ_name]
                mylist.append(myitem)

    df = pd.DataFrame(mylist)

    figure_output_path = 'results/compare.png'
    plt.figure(0,figsize=(10,10))
    viol_plot = sns.violinplot(x="dice",
                        y="organ",
                        hue="kind", 
                        data=df, 
                        palette="colorblind",
                        kind='violin',
                        size = 10,
                        aspect = 1.5,
                        legend_out=True)
    plt.grid(True)
    plt.savefig(figure_output_path)
    plt.close()

def save_age(root_folder,age_csv_file):

    file_list = []
    folder_list = [os.path.join(root_folder,x) for x in os.listdir(root_folder)]
    for folder_path in folder_list:
        tmplist = sorted(os.listdir(folder_path))
        if len(tmplist)==1:
            continue
        file_path = os.path.join(folder_path,tmplist[0])
        file_list.append(file_path)

    mylist =[]
    for file_path in tqdm(file_list):
        print(file_path)
        ds = pydicom.dcmread(file_path)
        myitem=dict(uid=ds.PatientID)

        for dcm_tag in ['PatientAge','PatientSex','PatientSize','PatientIdentityRemoved']:
            if dcm_tag in ds:
                tmp_val = ds[dcm_tag].value
                if dcm_tag == 'PatientAge':
                    tmp_val = int(tmp_val.replace('Y',''))
                myitem[dcm_tag] = tmp_val
            else:
                myitem[dcm_tag] = None
        if myitem['PatientAge'] is None:
            continue
        mylist.append(myitem)
        print(myitem)

    df = pd.DataFrame(mylist)
    df.to_csv(age_csv_file,index=False)

def results_with_age():
    
    # bad hard code BAD. not production. hardcode away.
    ped_ct_seg_dcm_root_folder = '/mnt/hd2/data/ped-ct-seg'
    age_csv_file = 'results/age.csv'
    if not os.path.exists(age_csv_file):
        save_age(ped_ct_seg_dcm_root_folder,age_csv_file)

    default_df = pd.read_csv('results/agg-default.csv')
    dicom_df = pd.read_csv(age_csv_file)

    mylist = []
    for uid in default_df.uid.unique():

        defaut_item = dict(default_df[default_df.uid==uid].iloc[0,:])
        dicom_item = dict(dicom_df[dicom_df.uid==uid].iloc[0,:])
        organ_list = sorted([x for x in defaut_item.keys() if x != 'uid'])
    
        for organ_name in organ_list:

            if np.isnan(defaut_item[organ_name]):
                continue
            myitem = dict(uid=uid)
            myitem['organ']=organ_name
            myitem['dice']=defaut_item[organ_name]
            myitem.update(dicom_item)
            mylist.append(myitem)

    df = pd.DataFrame(mylist)

    plt.figure(0,figsize=(20,10))
    viol_plot = sns.violinplot(
        data=df,x="organ",y="dice",hue="PatientAge",
        inner='box',scale='width', cut=1, linewidth=0.25, legend_out=True,
    )
    plt.xticks(rotation=45)
    plt.title(
        "Age plotted against dice by organ.\n"+\
        "(Dice between manual contours and TotalSegmentator predictions, dataset used Pediatric-CT-SEG n=~359.\n"+\
        "github@s: TotalSegmentator @wasserth, Pediatric-CT-SEG @jordanpn, plot by @pangyuteng 2022-12-26"
    )

    figure_output_path = "results/age-vs-dice-all.png"
    plt.grid(True)
    plt.savefig(figure_output_path)  
    plt.close()

    organ = "Liver"
    df = df[df.organ==organ]

    plt.figure(0,figsize=(20,10))
    viol_plot = sns.violinplot(
        data=df,x="organ",y="dice",hue="PatientAge",
        inner='box',scale='width', cut=1, linewidth=1, legend_out=True,
    )

    plt.title(
        f"Age plotted against dice in {organ}.\n"+\
        "(Dice between manual contours and TotalSegmentator predictions, dataset used Pediatric-CT-SEG n=~359.\n"+\
        "github@s: TotalSegmentator @wasserth, Pediatric-CT-SEG @jordanpn, plot by @pangyuteng 2022-12-26"
    )

    figure_output_path = f"results/age-vs-dice-{organ}.png"
    plt.grid(True)
    plt.savefig(figure_output_path)  
    plt.close()

if __name__ == "__main__":
    compare_results()
    results_with_age()

