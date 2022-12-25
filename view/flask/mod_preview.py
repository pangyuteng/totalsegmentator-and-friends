
import numpy as np
import pandas as pd
import imageio

def generate_mip(ct_data, mask_data, file_out):

    ct_data = ct_data.clip(-1000,1000)
    ct_mip = np.sum(ct_data,axis=-2)
    mymin,mymax = np.min(ct_mip),np.max(ct_mip)
    ct_mip = ((ct_mip-mymin)/(mymax-mymin)).clip(0,1)*255

    mask_mip = (np.max(mask_data,axis=-2)/104).clip(0,1)*255

    mythumbnail = np.concatenate([ct_mip,mask_mip],axis=1)
    mythumbnail = mythumbnail.astype(np.uint8)

    imageio.imwrite(file_out,mythumbnail)