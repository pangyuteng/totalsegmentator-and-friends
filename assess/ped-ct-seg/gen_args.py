import os
import sys
import warnings

root_folder = os.path.abspath(sys.argv[1])
csv_folder = os.path.abspath(sys.argv[2])

folder_list = [os.path.join(root_folder,x) for x in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder,x))]

mylist = []
for x in folder_list:
    image_file = os.path.join(x,'image.nii.gz')
    mask_file = os.path.join(x,'mask_preprocessed.nii.gz')
    if not os.path.exists(image_file):
        warnings.warn(f'missing image_file {x}')
        continue
    if not os.path.exists(mask_file):
        warnings.warn(f'missing mask_file {x}')
        continue
    item=dict(folder=x,image_file=image_file,mask_file=mask_file)
    mylist.append(item)

assert(len(mylist)==359)
#flags="--fast"
flags = ""
with open('inference.args','w') as f:
    for n,mydict in enumerate(mylist):
        item_folder = mydict['folder']
        image_file = os.path.join(item_folder,'image.nii.gz')
        seg_folder = os.path.join(item_folder,'segmentations')
        myline = f"{image_file} {seg_folder} {flags}\n"
        f.write(myline)

with open('process.args','w') as f:
    for n,mydict in enumerate(mylist):
        item_folder = mydict['folder']
        image_file = os.path.join(item_folder,'image.nii.gz')
        mask_file = os.path.join(item_folder,'mask_preprocessed.nii.gz')
        seg_folder = os.path.join(item_folder,'segmentations')
        seg_file = os.path.join(item_folder,'segmentations.nii.gz')
        json_file = os.path.join(item_folder,'scores.json')
        myline = f"{image_file} {mask_file} {seg_folder} {seg_file} {json_file}\n"
        f.write(myline)

with open('aggregate.args','w') as f:
    myline = f"{root_folder} {csv_folder} -p default\n"
    f.write(myline)

"""

docker run -it -u $(id -u):$(id -g) \
    -w $PWD -v /mnt:/mnt pangyuteng/ml:latest bash

python gen_args.py /mnt/hd2/data/ped-ct-seg-nifti results

docker run -it -u $(id -u):$(id -g) \
    -w $PWD -v /cvibraid:/cvibraid -v /radraid:/radraid \
    pangyuteng/ml:latest bash

python gen_args.py /radraid/pteng/ped-ct-seg-nifti results

"""
