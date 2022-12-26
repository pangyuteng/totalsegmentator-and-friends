import os
import sys
import json
import numpy as np
import SimpleITK as sitk

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
pedctseg_json_file = os.path.join(THIS_DIR,'pedctseg.json')
totalsegmentator_json_file = os.path.join(THIS_DIR,'totalsegmentator.json')
totalsegmentator2pedctseg_json_file = os.path.join(THIS_DIR,'totalsegmentator2pedctseg.json')

def load_mappers():
    with open(pedctseg_json_file,'r') as f:
        pedctseg_dict = json.loads(f.read())
    with open(totalsegmentator_json_file,'r') as f:
        totalsegmentator_dict = json.loads(f.read())
    with open(totalsegmentator2pedctseg_json_file,'r') as f:
        totalsegmentator2pedctseg_dict = json.loads(f.read())
    return pedctseg_dict, totalsegmentator_dict, totalsegmentator2pedctseg_dict
pedctseg_dict, totalsegmentator_dict, totalsegmentator2pedctseg_dict = load_mappers()

intersect_dict = {}
for k,v in pedctseg_dict.items():
    intersect_dict[k] = [q for q,t in totalsegmentator2pedctseg_dict.items() if t==v]
"""
# sample output for `intersect_dict`
intersect_dict = { ...
    "Thymus":[],
    "Lung_L":['lung_lower_lobe_left.nii.gz', 'lung_upper_lobe_left.nii.gz'],
... }
"""


def imread(file_path):
    reader= sitk.ImageFileReader()
    reader.SetFileName(file_path)
    my_obj = reader.Execute()
    return my_obj

def imwrite(file_path,my_arr,src_obj,use_compression=True):
    my_obj = sitk.GetImageFromArray(my_arr)
    my_obj.CopyInformation(src_obj)
    writer = sitk.ImageFileWriter()    
    writer.SetFileName(file_path)
    writer.SetUseCompression(use_compression)
    writer.Execute(my_obj)

def merge_masks(segmentation_folder,output_nifti_file):
    final_mask = None
    for basename in os.listdir(segmentation_folder):
        print('merge_masks',basename)
        if not basename.endswith('.nii.gz'):
            continue
        mask_file = os.path.join(segmentation_folder,basename)
        mask_obj = imread(mask_file)
        item_mask = sitk.GetArrayFromImage(mask_obj)
        if final_mask is None:
            final_mask = np.zeros_like(item_mask)
        int_val = totalsegmentator_dict[basename]
        final_mask[item_mask==1]=int_val

    imwrite(output_nifti_file,final_mask,mask_obj,use_compression=True)


# Dice similarity function
def dice_fn(y_true,y_pred):
    intersection = np.sum(y_pred[y_true==1]) * 2.0
    dice_score = intersection / (np.sum(y_pred) + np.sum(y_true))
    return dice_score

def main(image_nifti_file,mask_nifti_file,segmentation_folder,output_nifti_file,score_json_file):

    # merge masks
    if not os.path.exists(output_nifti_file):
        merge_masks(segmentation_folder,output_nifti_file)

    # compute dice
    score_dict = {"dice":{}}
    print('reading',mask_nifti_file)
    gt_obj = imread(mask_nifti_file)
    gt_mask = sitk.GetArrayFromImage(gt_obj)
    
    for organ_name,file_list in intersect_dict.items():
        print(organ_name)
        ped_val = pedctseg_dict[organ_name]
        absent = np.sum(gt_mask==ped_val) == 0
        if absent: # no ground truth (no y)
            score_dict["dice"][organ_name]=None
            print('    L---- absent')
            continue
        if len(file_list)==0: # no yhat
            score_dict["dice"][organ_name]=None
            continue
        y_true = gt_mask==ped_val
        y_pred = np.zeros_like(y_true)
        for basename in file_list:
            print(f'    {basename}')
            file_path = os.path.join(segmentation_folder,basename)
            mask_obj = imread(file_path)
            mask_arr = sitk.GetArrayFromImage(mask_obj)
            y_pred[mask_arr==1] = 1
        print(y_true.shape,y_pred.shape,np.sum(y_true),np.sum(y_pred))
        score_dict["dice"][organ_name]=dice_fn(y_true, y_pred)

        with open(score_json_file,"w") as f:
            f.write(json.dumps(score_dict,sort_keys=True,indent=4))

if __name__ == "__main__":
    image_nifti_file = sys.argv[1]
    mask_nifti_file = sys.argv[2]
    segmentation_folder = sys.argv[3]
    output_nifti_file = sys.argv[4]
    score_json_file = sys.argv[5]
    main(image_nifti_file,mask_nifti_file,segmentation_folder,output_nifti_file,score_json_file)

