
import os
import sys
import pandas as pd
from data_gen import readrow

def BAKreadrow(row):
    image_path = row.image_path
    seg_path = row.seg_path

    file_reader = sitk.ImageFileReader()
    file_reader.SetFileName(seg_path)
    file_reader.ReadImageInformation()
    image_size = file_reader.GetSize()


df = pd.read_csv('data.csv')
df['sitkerror']=None
while True:
    for n,row in df.iterrows():
        print(n)
        try:
            readrow(row)
            df.loc[n,'sitkerror']=False
        except KeyboardInterrupt:
            sys.exit(1)
        except:
            print('err')
            df.loc[n,'sitkerror']=True

if sys.argv[1]=='save':
    df.to_csv('data.csv',index=False)
