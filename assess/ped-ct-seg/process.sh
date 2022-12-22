#!/bin/bash
export image_nifti_file=$1
export mask_nifti_file=$2
export segmentation_folder=$3

python process.py $image_nifti_file $mask_nifti_file $segmentation_folder
