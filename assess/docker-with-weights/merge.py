import os
import sys
import SimpleITK

input_seg_folder = sys.argv[1]
#output_nifti_file = sys.argv[2]
name_list = sorted([x.replace(".nii.gz","") for x in os.listdir(input_seg_folder)])
print(name_list)