#!/bin/bash
export image_file=$1
export mask_file=$2
export seg_folder=$3
export seg_file=$4
export score_file=$5

python process.py $image_file $mask_file $seg_folder $seg_file $score_file
