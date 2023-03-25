import os
import sys
import time
import numpy as np
import SimpleITK as sitk

MYSIZE = 128
for x in range(10):
    fname = f'{x}.nii.gz'
    if not os.path.exists(fname):
        arr = np.random.rand(MYSIZE,MYSIZE,MYSIZE)
        img_obj = sitk.GetImageFromArray(arr)
        sitk.WriteImage(img_obj,fname)

def myread(x,thickness):

    image_path = fname = f'{x}.nii.gz'

    extract_size = [MYSIZE,MYSIZE,thickness]
    extract_index = [0,0,0]

    file_reader = sitk.ImageFileReader()
    file_reader.SetFileName(image_path)
    file_reader.SetExtractIndex(extract_index)
    file_reader.SetExtractSize(extract_size)
    image_obj = file_reader.Execute()
    img = sitk.GetArrayFromImage(image_obj)
    return img

for thickness in [10,1]:
    for x in range(10):
        myread(x,thickness)
    print('you have 20 seconds to run `lsof | grep nii.gz | wc -l`')
    time.sleep(20)

