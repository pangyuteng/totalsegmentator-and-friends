import pandas as pd
import SimpleITK as sitk
from data_gen import readrow

df = pd.read_csv('data.csv')
df['sitkerror']=None
for n,row in df.iterrows():
    print(n)
    try:
        readrow(row)
        df.loc[n,'sitkerror']=False
    except:
        print('err')
        df.loc[n,'sitkerror']=True
        
df.to_csv('data.csv',index=False)