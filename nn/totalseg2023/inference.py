import os
import sys
import ast
import random
import argparse
import numpy as np
import pandas as pd

import os,sys
import numpy as np
import tensorflow as tf
from data_gen import NUM_CLASSES, IMG_SIZE, TARGET_SHAPE, WH, THICKNESS, normalize_img

from model import get_model

from skimage.transform import resize
import SimpleITK as sitk
import pydicom

def inference(image_path,mask_path,weight_file):

    checkpoint_filepath = "checkpoint"

    model = get_model(IMG_SIZE,NUM_CLASSES)
    model.load_weights(weight_file)

    img_obj = sitk.ReadImage(image_path)
    print('---')
    print(img_obj.GetSize())
    print(img_obj.GetSpacing())
    print('---')
    image = sitk.GetArrayFromImage(img_obj)

    image = image.astype(np.float)
    image = normalize_img(image)

    original_shape = image.shape
    print('original_shape',original_shape)
    image = np.swapaxes(image,0,-1)
    print('axes swapped',image.shape)
    image_shape = image.shape
    chunks = np.ceil(image.shape[-1]/THICKNESS)
    print('chunks',chunks)
    inference_shape = (WH,WH,chunks*THICKNESS)
    arr = resize(image,inference_shape,order=0)
    print('post resize',arr.shape)
    arr = np.array_split(arr,chunks,axis=-1)
    arr = np.expand_dims(arr,axis=-1)
    print('post split',arr.shape)
    batch_size = 16
    out_arr = model.predict(arr,batch_size=batch_size)
    mask = (out_arr > 0.5).astype(np.int16).squeeze()
    print(np.unique(mask))
    print('mask.shape',mask.shape)
    mask = np.concatenate(mask,axis=-1)
    print('mask.shape',mask.shape)
    mask = mask.astype(np.float)
    mask = np.swapaxes(mask,0,-1)
    print('mask.shape',mask.shape)
    mask = resize(mask,original_shape,order=0)
    print('mask.shape',mask.shape)
    mask = mask.astype(np.int16)
    print(np.unique(mask))
    print(mask.shape)

    mask_obj = sitk.GetImageFromArray(mask)
    mask_obj.SetSpacing(img_obj.GetSpacing())
    mask_obj.SetOrigin(img_obj.GetOrigin())
    mask_obj.SetDirection(img_obj.GetDirection())

    writer = sitk.WriteImage(mask_obj,mask_path)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('image_path',type=str)
    parser.add_argument('mask_path',type=str)
    parser.add_argument('weight_file',type=str)

    args = parser.parse_args()
    inference(args.image_path,args.mask_path,args.weight_file)


'''
CUDA_VISIBLE_DEVICES=3 python inference.py /scratch2/personal/pteng-public/dataset/rawlung/RESEARCH/image/102779344.nii.gz lung-mask.nii.gz $weight_file
'''
