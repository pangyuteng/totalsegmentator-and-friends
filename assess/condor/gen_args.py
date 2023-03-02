import os
import sys
import pandas as pd

'''
input csv file needs to have 2 columns
output_folder_path
nifti_image_path
'''
csv_file = os.path.abspath(sys.argv[1])
df = pd.read_csv(csv_file)

mylist = []
for n,row in df.iterrows():
    totalseg_folder = os.path.join(row.output_folder_path,'segmentations')
    nifti_lung_path = os.path.join(row.output_folder_path,'segmentations','lung.nii.gz')
    item = dict(
        nifti_image_path=row.nifti_image_path,
        totalseg_folder=totalseg_folder,
    )
    mylist.append(item)

with open('my.args','w') as f:
    for n,x in enumerate(mylist):
        myline = f"na {x['nifti_image_path']} {x['totalseg_folder']}\n"
        f.write(myline)

"""
python gen_args.py tl.csv
"""