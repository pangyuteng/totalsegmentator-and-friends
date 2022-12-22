#!/bin/bash
export image_file=$1
export seg_folder=$2

# inference
TotalSegmentator -i ${image_file} -o ${seg_folder}
