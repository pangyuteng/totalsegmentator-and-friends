
import os
import sys
import traceback
import SimpleITK as sitk
import numpy as np
import pandas as pd

THICKNESS = 16

def readrow(row):
    image_path = row.image_path
    seg_path = row.seg_path

    file_reader = sitk.ImageFileReader()
    file_reader.SetFileName(seg_path)
    file_reader.ReadImageInformation()
    image_size = file_reader.GetSize()

    # attempt to augment z spacing to be within 0.4 to 5.4mm
    extract_size = list(file_reader.GetSize())
    current_index = [0] * file_reader.GetDimension()

    axis = int(np.random.choice([0,1,2]))

    mylist = np.arange(0,image_size[axis]-THICKNESS,1)
    idx = int(np.random.choice(mylist))
    current_index[axis] = idx
    extract_size[axis] = THICKNESS

    file_reader.SetFileName(image_path)
    file_reader.SetExtractIndex(current_index)
    file_reader.SetExtractSize(extract_size)
    image_obj = file_reader.Execute()

    file_reader.SetFileName(seg_path)
    file_reader.SetExtractIndex(current_index)
    file_reader.SetExtractSize(extract_size)
    mask_obj = file_reader.Execute()

    img = sitk.GetArrayFromImage(image_obj)
    mask = sitk.GetArrayFromImage(mask_obj)

    min_axis = int(np.argmin(img.shape))
    img = np.swapaxes(img,min_axis,-1)
    mask = np.swapaxes(mask,min_axis,-1)

    return img, mask


df = pd.read_csv('data.csv')

for n,row in df.iterrows():
    print(n)
    try:
        readrow(row)
    except KeyboardInterrupt:
        sys.exit(1)
    except:
        traceback.print_exc()