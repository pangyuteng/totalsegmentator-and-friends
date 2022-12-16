import os
import sys
import json
import argparse
import pandas as pd

from flask import (
    Flask, render_template, request, jsonify
)

app = Flask(__name__,
    static_url_path='/static',
    static_folder='static',
    template_folder='templates',
)
root_dir = os.environ.get('DATADIR')

@app.route('/review')
def review():
    case_id = request.args.get('case_id')
    case_folder = os.path.join(root_dir,case_id)

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

@app.route('/')
def home():
    case_list = [ {'case_id':x} for x in sorted(os.listdir(root_dir)) \
        if os.path.isdir(os.path.join(root_dir,x)) ]
    df = pd.DataFrame(case_list)
    return render_template("home.html",df=df)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--port",type=int,default=5000)
    args = parser.parse_args()
    app.run(debug=True,host="0.0.0.0",port=args.port)

"""
"""