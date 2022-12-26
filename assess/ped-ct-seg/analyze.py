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
    sns.set(style="ticks")

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

def results_with_age():
    default_df = pd.read_csv('results/agg-default.csv')
    dicom_df = pd.read_csv('results/age.csv')

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
        x="organ",
        y="dice",
        hue="PatientAge", 
        data=df, 
        palette="colorblind",
        kind='violin',
        size = 10,
        aspect = 1,
        legend_out=True)

    plt.title("Age plotted against dice.\n"+\
        "(Dice between manual contours and TotalSegmentator predictions, dataset used Pediatric-CT-SEG n=~359.\n"+\
        "github@s: TotalSegmentator @wasserth, Pediatric-CT-SEG @jordanpn, plot by @pangyuteng 2022-12-26"
        )

    figure_output_path = "results/age-vs-dice.png"
    plt.grid(True)
    plt.savefig(figure_output_path)  

if __name__ == "__main__":
    #compare_results()
    results_with_age()
