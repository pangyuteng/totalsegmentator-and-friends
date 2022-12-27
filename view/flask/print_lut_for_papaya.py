
import os
import sys
import json
import random
import numpy as np
random.seed(0)
rand_color = lambda: [np.round(random.random(),2),np.round(random.random(),2),np.round(random.random(),2)]

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def ped_ct_seg_lookup():
    pedctseg_folder = os.path.join(os.path.dirname(os.path.dirname(THIS_DIR)),'assess','ped-ct-seg')
    pedctseg_json_file = os.path.join(pedctseg_folder,'pedctseg.json')
    with open(pedctseg_json_file,'r') as f:
        pedctseg = json.loads(f.read())

    color_dict = {}
    pedctseg_color_list = [[0,0,0,0]]
    for k,v in pedctseg.items():
        
        color_dict[v]= rand_color()
        scaled_val = np.round(v/27,3)
        item = list(color_dict[v])
        item.insert(0, scaled_val)
        pedctseg_color_list.append(item)

    mapper_json_file = os.path.join(pedctseg_folder,'totalsegmentator2pedctseg.json')
    with open(mapper_json_file,'r') as f:
        mapper = json.loads(f.read())

    totalseg_color_list = [[0,0,0,0]]
    for n,organ_name in enumerate(sorted(mapper.keys())):
        v = mapper[organ_name]
        scaled_val = np.round((n+1)/104,3)
        if v == -1:
            item=[scaled_val,0,0,0]
        else:
            item = list(color_dict[v])
            item.insert(0, scaled_val)
        totalseg_color_list.append(item)

    print('insert to `CustomPedctseg` in `compared.html` for ped-ct-seg:')
    print(pedctseg_color_list)
    print('insert to `CustomTotalseg` in `compared.html` for ped-ct-seg:')
    print(totalseg_color_list)

def amos22_lookup():

    amos22_folder = os.path.join(os.path.dirname(os.path.dirname(THIS_DIR)),'assess','amos22')
    amos22_json_file = os.path.join(amos22_folder,'amos22.json')
    with open(amos22_json_file,'r') as f:
        amos22 = json.loads(f.read())

    color_dict = {}
    amos22_color_list = [[0,0,0,0]]
    # v needs to be incremental!
    for k,v in amos22.items():
        
        color_dict[v]= rand_color()
        scaled_val = np.round(v/15,3)
        item = list(color_dict[v])
        item.insert(0, scaled_val)
        amos22_color_list.append(item)

    mapper_json_file = os.path.join(amos22_folder,'totalsegmentator2amos22.json')
    with open(mapper_json_file,'r') as f:
        mapper = json.loads(f.read())

    totalseg_color_list = [[0,0,0,0]]
    for n,organ_name in enumerate(sorted(mapper.keys())):
        v = mapper[organ_name]
        scaled_val = np.round((n+1)/104,3)
        if v == -1:
            item=[scaled_val,0,0,0]
        else:
            item = list(color_dict[v])
            item.insert(0, scaled_val)
        totalseg_color_list.append(item)

    print('insert to `CustomAmos22` in `compared.html` for amos22:')
    print(amos22_color_list)
    print('insert to `CustomTotalseg` in `compared.html` for amos22:')
    print(totalseg_color_list)

ped_ct_seg_lookup()
amos22_lookup()

"""

docker run -it -u $(id -u):$(id -g) \
    -w $PWD -v /mnt:/mnt pangyuteng/ml:latest bash

python print_lut_for_papaya.py

"""