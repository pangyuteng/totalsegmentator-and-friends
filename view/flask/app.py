import os
import sys
import json
import argparse
from pathlib import Path
import pandas as pd
from flask import (
    Flask, render_template, request, jsonify
)
from utils import TOTALSEG_MAXVAL,load_json

DATADIR_TOTALSEG = os.environ.get('DATADIR_TOTALSEG')
DATADIR_PEDCTSEG = os.environ.get('DATADIR_PEDCTSEG')
DATADIR_AMOS22 = os.environ.get('DATADIR_AMOS22')
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,
    static_url_path='/static',
    static_folder='static',
    template_folder='templates',
)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/review')
def review():
    case_id = request.args.get('case_id')
    case_folder = os.path.join(DATADIR_TOTALSEG,case_id)

    image_file = os.path.join(case_folder,'ct.nii.gz')
    mask_file = os.path.join(case_folder,'segmentations.nii.gz')
    app.logger.info(image_file)
    app.logger.info(mask_file)
    return render_template("review.html",
        case_id = case_id,
        image_file = image_file,
        mask_file = mask_file,
        image_basename = os.path.basename(image_file),
        mask_basename = os.path.basename(mask_file),
    )

amos22_json_file = os.path.join(DATADIR_AMOS22,'dataset.json')
with open(amos22_json_file,'r') as f:
    amos22_dict = json.loads(f.read())
    amos22_train_list = [  os.path.basename(x['image']).replace(".nii.gz","") for x in amos22_dict['training']  ]
    amos22_val_list = [  os.path.basename(x['image']).replace(".nii.gz","") for x in amos22_dict['validation']  ]

""
@app.route('/compare')
def compare():
    case_id = request.args.get('case_id')
    dataset_name = request.args.get('dataset_name')

    if dataset_name == "ped-ct-seg":
        manual_max=27
        case_folder = os.path.join(DATADIR_PEDCTSEG,case_id)
        image_file = os.path.join(case_folder,'image.nii.gz')
        manual_mask_file = os.path.join(case_folder,'mask_preprocessed.nii.gz')
        totalseg_mask_file = os.path.join(case_folder,'segmentations.nii.gz')

    if dataset_name == "amos22":
        manual_max=15
        if case_id in amos22_train_list:
            img_folder = 'imagesTr'
            label_folder = 'labelsTr'
        elif case_id in amos22_val_list:
            img_folder = 'imagesVa'
            label_folder = 'labelsVa'
        else:
            raise NotImplemented()
        image_file = os.path.join(DATADIR_AMOS22,img_folder,f'{case_id}.nii.gz')
        src_manual_mask_file = os.path.join(DATADIR_AMOS22,label_folder,f'{case_id}.nii.gz')
        manual_mask_file = os.path.join(DATADIR_AMOS22,label_folder,f'{case_id}_mask.nii.gz')
        if not os.path.exists(manual_mask_file):
            os.symlink(src_manual_mask_file,manual_mask_file)

        root_dir = os.path.join(DATADIR_AMOS22,'totalseg')
        case_folder = os.path.join(root_dir,case_id)
        totalseg_mask_file = os.path.join(case_folder,'segmentations.nii.gz')

    dataset_lut_file = os.path.join(THIS_DIR,'static',f'dataset-{dataset_name}.json')
    totalseg_lut_file = os.path.join(THIS_DIR,'static',f'totalseg-{dataset_name}.json')
    dataset_lut = load_json(dataset_lut_file)
    totalseg_lut = load_json(totalseg_lut_file)
    dataset_max = len(dataset_lut)-1 # minus 1 for "color of value 0" in lut

    app.logger.info(image_file)
    app.logger.info(manual_mask_file)
    app.logger.info(totalseg_mask_file)

    return render_template("compare.html",
        dataset_name = dataset_name,
        dataset_max=dataset_max,
        dataset_lut=dataset_lut,
        totalseg_max=TOTALSEG_MAXVAL,
        totalseg_lut=totalseg_lut,
        case_id = case_id,
        image_file = image_file,
        manual_mask_file = manual_mask_file,
        totalseg_mask_file = totalseg_mask_file,
        image_basename = os.path.basename(image_file),
        manual_mask_basename = os.path.basename(manual_mask_file),
        totalseg_mask_basename = os.path.basename(totalseg_mask_file),
    )

@app.route('/')
def home():
    url_list = ['totalsegmentator','pet_ct_seg','amos22']
    return render_template("home.html",url_list=url_list)

@app.route('/totalsegmentator')
def totalsegmentator():
    case_list = [ {'case_id':x,"png_url": os.path.join(DATADIR_TOTALSEG,x,"thumbnail_0.png")} \
        for x in sorted(os.listdir(DATADIR_TOTALSEG)) \
        if os.path.isdir(os.path.join(DATADIR_TOTALSEG,x)) ]
    df = pd.DataFrame(case_list)
    return render_template("totalsegmentator.html",df=df)

@app.route('/pet-ct-seg')
def pet_ct_seg():
    json_file_list = []
    for path in Path(DATADIR_PEDCTSEG).rglob("*scores.json"):
        json_file_list.append(str(path))
    json_file_list = sorted(json_file_list)
    mylist = []
    organ_list = None
    for json_file in json_file_list:

        with open(json_file,'r') as f:
            results_dict = json.loads(f.read())

        if organ_list is None:
            organ_list = sorted(list(results_dict['dice'].keys()))

        case_id = os.path.basename(os.path.dirname(json_file))
        item = dict(
            case_id=case_id,
        )
        for organ_name in organ_list:
            if organ_name in results_dict['dice'].keys():
                item[organ_name]=results_dict['dice'][organ_name]
            else:
                item[organ_name]="NA"
        mylist.append(item)

    df = pd.DataFrame(mylist)
    df["case_id"] = df["case_id"].apply(
        lambda x: f"""<a href="/compare?case_id={x}&dataset_name=ped-ct-seg">{x}</a>"""
    )
    table = df.to_html(
        table_id="my_table",index=False,header="true",
        classes="display",border=0,
        render_links=True,escape=False,
    )

    return render_template("pet_ct_seg.html",df=df,table=table)

@app.route('/amos22')
def amos22():
    root_dir = os.path.join(DATADIR_AMOS22,'totalseg')
    json_file_list = []
    for path in Path(root_dir).rglob("*scores.json"):
        json_file_list.append(str(path))
    json_file_list = sorted(json_file_list)
    mylist = []
    organ_list = None
    for json_file in json_file_list:

        with open(json_file,'r') as f:
            results_dict = json.loads(f.read())

        if organ_list is None:
            organ_list = sorted(list(results_dict['dice'].keys()))

        case_id = os.path.basename(os.path.dirname(json_file))
        item = dict(
            case_id=case_id,
        )
        for organ_name in organ_list:
            if organ_name in results_dict['dice'].keys():
                item[organ_name]=results_dict['dice'][organ_name]
            else:
                item[organ_name]="NA"
        mylist.append(item)

    df = pd.DataFrame(mylist)
    df["case_id"] = df["case_id"].apply(
        lambda x: f"""<a href="/compare?case_id={x}&dataset_name=amos22">{x}</a>"""
    )
    table = df.to_html(
        table_id="my_table",index=False,header="true",
        classes="display",border=0,
        render_links=True,escape=False,
    )

    return render_template("amos22.html",df=df,table=table)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--port",type=int,default=5000)
    args = parser.parse_args()
    app.run(host="0.0.0.0",port=args.port,debug=True)

"""
"""