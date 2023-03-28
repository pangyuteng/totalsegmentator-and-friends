import os
import sys
import numpy as np
import SimpleITK as sitk
from totalsegmentator.libs import combine_masks_to_multilabel_file

if __name__ == "__main__":
    input_seg_folder = sys.argv[1]
    output_nifti_file = sys.argv[2]
    combine_masks_to_multilabel_file(input_seg_folder,output_nifti_file)


