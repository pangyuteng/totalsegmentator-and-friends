import SimpleITK as sitk
import numpy as np

spacing = (0.8,0.8,1.6)
origin = (0.0,0.0,0.0)
direction = (1,0,0,0,1,0,0,0,1)
shape = (10,512,512)
img = (np.random.rand(*shape)*255).astype(np.int16)
nifti_file_path = 'blank.nii.gz'

img_obj = sitk.GetImageFromArray(img)
img_obj.SetSpacing(spacing)
img_obj.SetOrigin(origin)
img_obj.SetDirection(direction)

writer = sitk.ImageFileWriter()    
writer.SetFileName(nifti_file_path)
writer.SetUseCompression(True)
writer.Execute(img_obj)