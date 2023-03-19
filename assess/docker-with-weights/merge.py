import os
import sys
import numpy as np
import SimpleITK as sitk

input_seg_folder = sys.argv[1]
output_nifti_file = sys.argv[2]


from totalsegmentator.libs import combine_masks_to_multilabel_file

combine_masks_to_multilabel_file(input_seg_folder,output_nifti_file)
