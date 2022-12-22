#!/bin/bash
export image_file=$1
export seg_folder=$2

export liver_file=${seg_folder}/liver.nii.gz
if [ -f ${liver_file} ]; then
    echo "File found!"
    exit 0
fi
# inference
TotalSegmentator -i ${image_file} -o ${seg_folder}
