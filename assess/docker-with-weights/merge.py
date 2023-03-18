import os
import sys
import numpy as np
import SimpleITK as sitk

input_seg_folder = sys.argv[1]
output_nifti_file = sys.argv[2]

# https://github.com/wasserth/TotalSegmentator/blob/0fbde4ff5029297ff60334830d7f134daeb845a9/totalsegmentator/preview.py
mask_file_list = [os.path.join(input_seg_folder,x) for x in os.listdir(input_seg_folder)]
tmp_obj = sitk.ReadImage(mask_file_list[0])
mask = np.zeros_like(sitk.GetArrayFromImage(tmp_obj)).astype(np.int16)
for n,mask_file in enumerate(mask_file_list):
    print(mask_file)
    tmp_obj = sitk.ReadImage(mask_file)
    tmp = sitk.GetArrayFromImage(tmp_obj)
    mask[tmp==1]=n+1
mask = mask.astype(np.int16)
mask_obj = sitk.GetImageFromArray(mask)
mask_obj.CopyInformation(tmp_obj)
sitk.WriteImage(mask_obj,output_nifti_file)
