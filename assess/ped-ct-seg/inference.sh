#!/bin/bash
export image_nifti_file=$1
export segmentation_folder=$2

# inference
TotalSegmentator -i ${image_nifti_file} -o ${segmentation_folder}
