#!/bin/bash
export INPUT_NIFTI_FILE=$1
export OUTPUT_NIFTI_FOLDER=$2
export LIVER_FILE=${OUTPUT_NIFTI_FOLDER}/liver.nii.gz

if [ ! -f ${LIVER_FILE} ]; then
    TotalSegmentator -i ${INPUT_NIFTI_FILE} -o ${OUTPUT_NIFTI_FOLDER}
fi
