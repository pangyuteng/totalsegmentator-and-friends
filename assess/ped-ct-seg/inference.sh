#!/bin/bash
export image_file=$1
export seg_folder=$2

export file_count=$(ls ${seg_folder} | wc -l)
if [ "${file_count}" -eq 104 ]; then
    echo "All 104 iles found!"
    exit 0
fi

# inference
TotalSegmentator -i ${image_file} -o ${seg_folder}
