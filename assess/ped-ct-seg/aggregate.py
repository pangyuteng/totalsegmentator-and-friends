import os
import sys
from pathlib import Path
import json
import pandas as pd

def main(root_folder):
    json_file_list = []
    for path in Path(root_folder).rglob("*scores.json"):
        json_file_list.append(str(path))

    mylist = []
    for x in json_file_list:
        print(x)
        with open(x,'r') as f:
            scores_dict = json.loads(f.read())
        mylist.append(scores_dict['dice'])

    df = pd.DataFrame(mylist)
    df.to_csv('agg.csv',index=False)

if __name__ == "__main__":
    # root folder
    root_folder = sys.argv[1]
    main(root_folder)

"""
docker run -it -u $(id -u):$(id -g) \
    -w $PWD -v /cvibraid:/cvibraid -v /radraid:/radraid \
    pangyuteng/ml:latest bash

python aggregate.py /radraid/pteng/ped-ct-seg-nifti
"""
