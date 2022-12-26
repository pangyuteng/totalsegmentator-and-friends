import os
import sys
import warnings
import json

root_folder = os.path.abspath(sys.argv[1])
csv_folder = os.path.abspath(sys.argv[2])

json_file = os.path.join(root_folder,'dataset.json')
with open(json_file,'r') as f:
    dataset_dict = json.loads(f.read())

label_dict = dataset_dict['labels']
# {"0": "background", "1": "spleen","2": "right kidney", "3": "left kidney", "4": "gall bladder", "5": "esophagus", "6": "liver", "7": "stomach", "8": "arota", "9":

mylist = []
mylist.extend(dataset_dict['training'])
mylist.extend(dataset_dict['validation'])
mylist.extend(dataset_dict['test'])

for myitem in mylist:

    if 'label' not in myitem.keys():
        continue

    image_file = os.path.abspath(os.path.join(root_folder,myitem['image']))
    mask_file = os.path.abspath(os.path.join(root_folder,myitem['label']))
    if not os.path.exists(image_file):
        warnings.warn(f'missing image_file {x}')
        continue
    if not os.path.exists(mask_file):
        warnings.warn(f'missing mask_file {x}')
        continue
    case_id = os.path.basename(image_file).replace('.nii.gz','')
    case_folder = os.path.join(root_folder,'totalseg',case_id)
    os.makedirs(seg_folder,exist_ok=True)
    item=dict(image_file=image_file,mask_file=mask_file,case_folder=case_folder)
    mylist.append(item)

assert(len(mylist)==960)

flags = ""
with open('inference.args','w') as f:
    for n,mydict in enumerate(mylist):
        case_folder = mydict['case_folder']
        image_file = mydict['image_file']
        seg_folder = os.path.join(case_folder,'segmentations')
        myline = f"{image_file} {seg_folder} {flags}\n"
        f.write(myline)

with open('process.args','w') as f:
    for n,mydict in enumerate(mylist):
        case_folder = mydict['case_folder']
        image_file = mydict['image_file']
        mask_file = mydict['mask_file']
        seg_folder = os.path.join(case_folder,'segmentations')
        seg_file = os.path.join(case_folder,'segmentations.nii.gz')
        json_file = os.path.join(case_folder,'scores.json')
        myline = f"{image_file} {mask_file} {seg_folder} {seg_file} {json_file}\n"
        f.write(myline)

with open('aggregate.args','w') as f:
    myline = f"{root_folder} {csv_folder} -p default\n"
    f.write(myline)

"""

docker run -it -u $(id -u):$(id -g) \
    -w $PWD -v /mnt:/mnt pangyuteng/ml:latest bash

python gen_args.py /mnt/scratch/data/amos22 results


"""
