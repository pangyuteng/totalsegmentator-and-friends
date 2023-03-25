import os
import sys
import time
import numpy as np
import SimpleITK as sitk

MYSIZE = 128
for x in range(20):
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

for thickness in [1,10]:
    for x in range(20):
        myread(x,thickness)
    print('you have 5 seconds to run `lsof | grep nii.gz | wc -l`')
    time.sleep(5)

