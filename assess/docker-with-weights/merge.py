#!/opt/conda/bin/python
import os
import sys
import numpy as np
import SimpleITK as sitk
from totalsegmentator.libs import combine_masks_to_multilabel_file
import SimpleITK as sitk
from scipy import ndimage
from skimage import measure

def gen_ghetto_body(image_nifti_file,output_nifti_file):

    mask_obj = sitk.ReadImage(output_nifti_file)
    mask = sitk.GetArrayFromImage(mask_obj)

    img_obj = sitk.ReadImage(image_nifti_file)
    img = sitk.GetArrayFromImage(img_obj)
    # body
    procarr = (img > -300).astype(np.int)
    procarr = ndimage.morphology.binary_closing(procarr,iterations=1)

    label_image, num = ndimage.label(procarr)
    region = measure.regionprops(label_image)
    region = sorted(region,key=lambda x:x.area,reverse=True)

    for r in region: # should just be 1 or 2
        tmpmask = label_image==r.label
        contain_body = np.sum(tmpmask) # maybe need to consider bkgd touching iamge border?
        if contain_body > 0:
            mask[np.logical_and(tmpmask==1,mask==0)]=105
            break

    mask_obj = sitk.GetImageFromArray(mask)
    mask_obj.CopyInformation(img_obj)
    sitk.WriteImage(mask_obj,output_nifti_file)

if __name__ == "__main__":
    image_nifti_file = sys.argv[1]
    input_seg_folder = sys.argv[2]
    output_nifti_file = sys.argv[3]
    combine_masks_to_multilabel_file(input_seg_folder,output_nifti_file)
    gen_ghetto_body(image_nifti_file,output_nifti_file)


