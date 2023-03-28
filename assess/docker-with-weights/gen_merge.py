import os
from pathlib import Path

def gen_merge():
    root = '/mnt/scratch/data/Totalsegmentator_dataset'
    image_path_list = [str(x) for x in Path(root).rglob("ct.nii.gz")]
    
    for img_file in image_path_list:
        seg_folder = os.path.join(os.path.dirname(img_file),'segmentations')
        seg_file = os.path.join(os.path.dirname(img_file),'segmentations.nii.gz')
        mystr = f'{img_file} {seg_folder} {seg_file}'
        print(mystr)


gen_merge()

'''

python gen_merge.py > my.args
condor_submit merge.sub

TotalSegmentator -i /mnt/scratch/data/Totalsegmentator_dataset/s1348/ct.nii.gz -o  /mnt/scratch/data/Totalsegmentator_dataset/s1348/segmentations -ta body
'''
