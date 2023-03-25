
import os
import sys
import time
import ast
from pathlib import Path
import numpy as np
import pandas as pd
import random
import imageio
from tensorflow.keras.utils import Sequence
import tensorflow as tf
from skimage.transform import resize 
from scipy import ndimage as ndi
import cv2
import albumentations as A
import SimpleITK as sitk
from keras.utils.np_utils import to_categorical

from sklearn.model_selection import train_test_split


def seed_everything(seed=4269):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    os.environ['TF_CUDNN_DETERMINISTIC'] = '1'  # new flag present in tf 2.0+
    np.random.seed(seed)
    tf.random.set_seed(seed)
seed_everything()

organ_mapper = dict(
    lung=1,
    clavicula=2,
    scapula=2,
    rib=2,
    vertebrae=2,
    femur=2,
    humerus=2,
    liver=3,
    spleen=4,
    kidney=5,
    stomach=6,
    duodenum=7,
    small_bowel=8,
    colon=9,
    pancreas=10,
    trachea=11,
    aorta=12,
    heart=13,
    pulmonary_artery=14,
    esophagus=15,
    lung_vessels=16,
    consolidation=17,
)

NUM_CLASSES = max(organ_mapper.values())+1
WH = 256
THICKNESS = 4
TARGET_SHAPE = (WH,WH,THICKNESS)
IMG_SIZE = (WH,WH,THICKNESS,1)

def readrow(row):
    image_path = row.image_path
    seg_path = row.seg_path

    file_reader = sitk.ImageFileReader()
    file_reader.SetFileName(image_path)
    file_reader.ReadImageInformation()
    image_size = file_reader.GetSize()

    # attempt to augment z spacing to be within 0.4 to 5.4mm
    extract_size = list(file_reader.GetSize())
    current_index = [0] * file_reader.GetDimension()

    axis = int(np.random.choice([0,1,2]))

    mylist = np.arange(0,image_size[axis]-THICKNESS,1)
    idx = int(np.random.choice(mylist))
    current_index[axis] = idx
    extract_size[axis] = THICKNESS

    file_reader.SetFileName(image_path)
    file_reader.SetExtractIndex(current_index)
    file_reader.SetExtractSize(extract_size)
    image_obj = file_reader.Execute()

    file_reader.SetFileName(seg_path)
    file_reader.SetExtractIndex(current_index)
    file_reader.SetExtractSize(extract_size)
    mask_obj = file_reader.Execute()

    img = sitk.GetArrayFromImage(image_obj)
    mask = sitk.GetArrayFromImage(mask_obj)

    min_axis = int(np.argmin(img.shape))
    img = np.swapaxes(img,min_axis,-1)
    mask = np.swapaxes(mask,min_axis,-1)

    return img, mask

MIN_VAL,MAX_VAL = -1000,1000
def normalize_img(img):
    img = ((img-MIN_VAL)/(MAX_VAL-MIN_VAL)).clip(0,1)
    return img

aug_pipeline = A.Compose([
    A.GridDistortion(p=0.5, num_steps=5),
    A.ShiftScaleRotate(border_mode=cv2.BORDER_CONSTANT,value=0, mask_value=0,scale_limit=(0.0,0.5)),
])
cutout_aug_pipeline = A.Compose([
    A.Cutout(p=0.25, num_holes=7, max_h_size=32, max_w_size=32, fill_value=0),
])

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(THIS_DIR,'data.csv')

class MySeriGenerator(Sequence):
    def __init__(self,kind,ret_option=0,batch_size=9,shuffle=False,augment=False):
        
        gen_csv() # prepare
        self.df = pd.read_csv(CSV_FILE,dtype=str)
        self.df = self.df[self.df.kind==kind]
        self.df = self.df.reset_index()
        print(self.df.index,len(self.df.index))

        self.indices = np.arange(len(self.df))

        self.batch_size = batch_size
        self.shuffle = shuffle
        self.augment = augment
        self.ret_option = ret_option

    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.indices)

    def dataread(self, row):
        img, mask = readrow(row)

        # image size varies, thus add padding prior resize.
        padding = None
        # pad 0
        if (img.shape[1]-img.shape[0])/img.shape[1] > 0.2:
            padding = [(0,0),(0,0),(0,0)]
            val = (img.shape[1]-img.shape[0])//2
            padding[0]=(val,val)
        # pad 1
        if (img.shape[0]-img.shape[1])/img.shape[0] > 0.2:
            padding = [(0,0),(0,0),(0,0)]
            val = (img.shape[0]-img.shape[1])//2
            padding[1]=(val,val)
        if padding:
            img = np.pad(img, padding, 'constant', constant_values=MIN_VAL)
            mask = np.pad(mask, padding, 'constant', constant_values=0)

        img = img.astype(np.float16)
        img = resize(img,TARGET_SHAPE,order=0)
        img = normalize_img(img)

        mask = mask.astype(np.float16)
        mask = resize(mask,TARGET_SHAPE,order=0,anti_aliasing=False,preserve_range=True).astype(int)
        
        if self.augment:
            augmented = aug_pipeline(
                image=img,
                mask=mask,
            )
            img = augmented['image']
            mask = augmented['mask']

            c_augmented = cutout_aug_pipeline(
                image=img,
            )
            cutout_img = c_augmented['image']
        else:
            cutout_img = img
            
        img = np.expand_dims(img,axis=-1)
        cutout_img = np.expand_dims(cutout_img,axis=-1)

        mask = mask.astype(np.uint8)
        mask = to_categorical(mask, num_classes=NUM_CLASSES)
        if self.ret_option == 0:
            mask[:,:,:,0] = -1
        img = img.astype(float)
        cutout_img = cutout_img.astype(float)
        mask = mask.astype(float)
        return img,cutout_img,mask

    def __len__(self):
        return int(np.floor(len(self.indices) / float(self.batch_size)))

    def __getitem__(self, idx):
        inds = self.indices[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_rows = self.df.iloc[inds,:]
        # read your data here using the batch lists, batch_x and batch_y
        x_arr = []
        cutout_x_arr = []
        mask_arr = []
        for n,row in batch_rows.iterrows():
            img,cutout_img,mask = self.dataread(row)
            x_arr.append(img)
            cutout_x_arr.append(cutout_img)
            mask_arr.append(mask)

        return np.array(cutout_x_arr), np.array(mask_arr)


def gen_csv():
    RAW_CSV_FILE = 'raw.csv'

    if not os.path.exists(RAW_CSV_FILE):
        root = '/radraid/pteng/Totalsegmentator_dataset'
        image_path_list = [str(x) for x in Path(root).rglob("ct.nii.gz")]

        mylist = []
        for image_path in image_path_list:
            print(image_path)
            file_reader = sitk.ImageFileReader()
            file_reader.SetFileName(image_path)
            file_reader.ReadImageInformation()
            image_size = file_reader.GetSize()
            image_spacing = file_reader.GetSpacing()
            mylist.append({
                "image_path": image_path,
                "image_size": image_size,
                "image_spacing": image_spacing,
            })
        pd.DataFrame(mylist).to_csv(RAW_CSV_FILE,index=False)

    if not os.path.exists(CSV_FILE):
        rawdf = pd.read_csv(RAW_CSV_FILE)
        # v1 train-test-split stratify by disease and mean-hu with smaller bin.
        # for each disease group
        #sort by mean_hu per 10hu bin, and by disease
        rawdf['seg_path']=None
        for n,row in rawdf.iterrows():
            seg_folder = row.image_path.replace("ct.nii.gz",'segmentations')
            seg_path = os.path.join(os.path.dirname(seg_folder),'merged.nii.gz')
            if os.path.exists(seg_path):
                rawdf.loc[n,'seg_path']=seg_path
                continue
            liver_file = os.path.join(seg_folder,'liver.nii.gz')
            if len(os.listdir(seg_folder)) >= 104:
                liver_obj = sitk.ReadImage(liver_file)
                mask = np.zeros_like(sitk.GetArrayFromImage(liver_obj))
                for basename in sorted(os.listdir(seg_folder)):
                    for organ_phrase, organ_value in organ_mapper.items():
                        if organ_phrase not in basename:
                            continue
                        organ_path = os.path.join(seg_folder,basename)
                        organ_obj = sitk.ReadImage(organ_path)
                        organ = sitk.GetArrayFromImage(organ_obj)
                        mask[organ>0]=organ_value

                mask_obj = sitk.GetImageFromArray(mask)
                mask_obj.CopyInformation(liver_obj)
                sitk.WriteImage(mask_obj,seg_path)
                rawdf.loc[n,'seg_path']=seg_path
                print(seg_path)
                print('--')

        print(rawdf.shape)
        rawdf.image_size = rawdf.image_size.apply(lambda x: ast.literal_eval(x))
        rawdf.image_spacing = rawdf.image_spacing.apply(lambda x: ast.literal_eval(x))
        rawdf = rawdf[
            (rawdf.seg_path.notnull()) & \
            (rawdf.image_size.apply(lambda x: x[-1] >= 50)) & \
            (rawdf.image_spacing.apply(lambda x: x[-1] < 10 ))  ]
        print(rawdf.shape)
        # rawdf['stratify'] = rawdf.index//25
        rawdf.sort_values(['image_size'],ignore_index=True,inplace=True,ascending=False)
        rawdf['stratify'] = rawdf.index//25
        rawdf['kind'] = None

        if False:
            for n,row in rawdf.iterrows():
                print(n,row.disease,row.mean_hu,row.stratify)
        
        X_tv, X_test, y_tv, y_test = train_test_split(list(rawdf.index), list(rawdf.stratify), test_size=0.1, random_state=42, stratify=rawdf.stratify)
        X_train, X_validation, y_train, y_validation = train_test_split(X_tv,y_tv,test_size=0.11111, random_state=42,stratify=y_tv)
        
        rawdf.loc[X_train,'kind']='train'
        rawdf.loc[X_validation,'kind']='validation'
        rawdf.loc[X_test,'kind']='test'
        
        df = rawdf[['image_path', 'seg_path','kind']]
        df = df.dropna()
        df.to_csv('data.csv',index=False)


if __name__ == "__main__":
    mygen = MySeriGenerator('validation',shuffle=True,augment=True)
    mygen = MySeriGenerator('test',shuffle=True,augment=True)
    mygen = MySeriGenerator('train',ret_option=1,shuffle=True,augment=True)
    mygen.on_epoch_end()
    os.makedirs('tmp',exist_ok=True)
    for x in range(2):
        img, mask = mygen[x]
        print(img.shape,mask.shape)
        idx = 4
        for y in range(img.shape[0]):
            scaled_img = img[y,:,:,idx].squeeze()
            scaled_mask = np.argmax(mask[y,:,:,idx,:].squeeze(),-1)/NUM_CLASSES
            merged = np.concatenate([scaled_img,scaled_mask],axis=1)
            merged = (merged*255).clip(0,255).astype(np.uint8)
            print(y,merged.shape)
            imageio.imwrite(f'tmp/viz-{x}-{y}.png',merged)

'''

docker run -it -u $(id -u):$(id -g) -w $PWD -v /mnt:/mnt pangyuteng/lungseg2023:latest bash
python data_gen.py

'''