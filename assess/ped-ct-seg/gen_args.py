import os
import sys

# root folder
root_folder = sys.argv[1]

folder_list = [os.path.join(root_folder,x) for x in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder,x))]
#assert(len(folder_list)==359)

mylist = []
for x in folder_list:
    image_file = os.path.join(x,'image.nii.gz')
    mask_file = os.path.join(x,'mask_preprocessed.nii.gz')
    if not os.path.exists(image_file):
        print('missing image_file',x)
        continue
    if not os.path.exists(mask_file):
        print('missing mask_file',x)
        continue
    item=dict(image_file=image_file,mask_file=mask_file)
    mylist.append(item)

/radraid/pteng/ped-ct-seg-nifti/Pediatric-CT-SEG-C26BBB5F/image.nii.gz /radraid/pteng/ped-ct-seg-nifti/Pediatric-CT-SEG-C26BBB5F/segmentations

/radraid/pteng/ped-ct-seg-nifti/Pediatric-CT-SEG-355/image.nii.gz /radraid/pteng/ped-ct-seg-nifti/Pediatric-CT-SEG-355/segmentations /radraid/pteng/ped-ct-seg-nifti/Pediatric-CT-SEG-355/segmentations.nii.gz

"""

python gen_args.py /radraid/pteng/ped-ct-seg-nifti
"""