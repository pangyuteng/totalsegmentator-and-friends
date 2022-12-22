#!/bin/bash
export image_file=$1
export seg_folder=$2

export file_count=$(ls ${seg_folder}/*.nii.gz | wc -l)
if [ "${file_count}" -eq 104 ]; then
    echo "All 104 files found, skipping inference!"
    exit 0
fi

# inference
echo TotalSegmentator -i ${image_file} -o ${seg_folder}
TotalSegmentator -i ${image_file} -o ${seg_folder}
