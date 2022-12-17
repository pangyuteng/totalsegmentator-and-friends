import sys
import os
import itertools
import pickle
from pathlib import Path

#import nibabel as nib
import numpy as np
import pandas as pd
from tqdm import tqdm
from fury import window, actor, ui, io, utils

from totalsegmentator.vtk_utils import contour_from_roi_smooth, plot_mask
from totalsegmentator.map_to_binary import class_map
np.random.seed(1234)
random_colors = np.random.rand(104, 4)

def plot_roi_group(ct_data, mask_data, scene, x, y, smoothing, task_name, affine=None):
    roi_actors = []

    for idx in range(104):
        color = random_colors[idx]
        data = mask_data == idx
        if data.max() > 0:  # empty mask
            affine[:3, 3] = 0  # make offset the same for all subjects
            cont_actor = plot_mask(scene, data, affine, x, y, smoothing=smoothing,
                                color=color, opacity=1)
            scene.add(cont_actor)
            roi_actors.append(cont_actor)

def plot_subject(ct_data, mask_data, output_path, smoothing=20,task_name="total"):
    subject_width = 330
    # subject_height = 700
    nr_cols = 10

    window_size = (1800, 400)

    scene = window.Scene()
    showm = window.ShowManager(scene, size=window_size, reset_camera=False)
    #showm.initialize()

    data = ct_data
    data = data.transpose(1, 2, 0)  # Show sagittal view
    data = data[::-1, :, :]
    value_range = (-115, 225)  # soft tissue window
    affine = [
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,0],
        [0,0,0,0],
    ]
    affine = np.array(affine)

    slice_actor = actor.slicer(data, affine, value_range)
    slice_actor.SetPosition(0, 0, 0)
    scene.add(slice_actor)

    # Plot 3D rois
    idx = 0
    x = (idx % nr_cols) * subject_width
    y = 0
    plot_roi_group(ct_data, mask_data, scene, x, y, smoothing, task_name, affine=affine)
    
    scene.projection(proj_type='parallel')
    scene.reset_camera_tight(margin_factor=1.02)  # need to do reset_camera=False in record for this to work in

    #window.record(scene, size=window_size,
    #              out_path=output_path, reset_camera=False)  # , reset_camera=False
    window.snapshot(scene,fname=output_path,size=window_size,offscreen=True)
    scene.clear()


def generate_preview(ct_data, mask_data, file_out, smoothing=20, task_name="total"):
    from xvfbwrapper import Xvfb
    # do not set random seed, otherwise can not call xvfb in parallel, because all generate same tmp dir
    with Xvfb() as xvfb:
        plot_subject(ct_data, mask_data, file_out, smoothing=smoothing, task_name=task_name)
