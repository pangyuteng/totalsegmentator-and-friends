"""
util to run to view Totalsegmentator_dataset with itksnap:
itksnap -g ct.nii.gz -s segmentations.nii.gz -l totalsegmentator_label.txt
"""
import os
import sys
import SimpleITK as sitk

def main(root_dir):
    pass
if __name__ == "__main__":
    root_dir = sys.argv[1]
    main(root_dir):