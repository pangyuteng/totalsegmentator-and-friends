#!/bin/bash
export image_file=$1
export mask_file=$2
export seg_folder=$3
export seg_file=$4
export score_file=$5

export file_count=$(ls ${seg_folder}/*.nii.gz | wc -l)
if [ "${file_count}" -ne 104 ]; then
    echo "inference not yet done!"
    exit 1
fi

if [ -f ${score_file} ]; then
    echo "json file found, skipping process.py!"
    exit 0
fi

python process.py $image_file $mask_file $seg_folder $seg_file $score_file

