
import os
import sys
from tqdm import tqdm
import pydicom
import pandas as pd

def main():
    root_folder = '/mnt/hd2/data/ped-ct-seg'
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
        mylist.append(myitem)
        print(myitem)

    df = pd.DataFrame(mylist)
    df.to_csv('results/age.csv')


if __name__ == "__main__":
    main()