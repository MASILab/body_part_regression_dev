"""
A pipeline software for bodypart regression and preprocessing

Yucheng Tang
OCT 2018

"""
from __future__ import print_function
import os
import numpy as np
#import caffe
import nibabel as nb
from nibabel.processing import resample_from_to 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image

from pre_bodypart_regression import Pre_bodypart
from bodypart_regression import Bodypart_regressor
from post_bodypart import post_bodypart_regression

import torch
import torch._utils
from monai.apps import download_url


### ---------- Parameters ---------- ###
import argparse
parser = argparse.ArgumentParser(description='Scripts pipeline for abodomen CT preprocessing')
# All working dirs

parser.add_argument('--root_path',  default='/home/yucheng/yucheng/2022/bpr_pipeline', 
                    help='root path for working folder')
parser.add_argument('--data_dir',  default='/home/yucheng/yucheng/2022/bpr_pipeline/datasets', 
                    help='root path for first volume which contains the middle index ')
# parser.add_argument('--checkpoint_dir', default= '/home/yucheng/yucheng/2022/bpr_pipeline/checkpoint',
#                     help='Folder that store all preprocessed niftis for training')  
parser.add_argument('--checkpoint_BPR', default= '/home/yucheng/yucheng/2022/bpr_pipeline/checkpoint_BPR/model.pth',
                    help='Folder that store all preprocessed niftis for training')  

parser.add_argument('--score_interval', default='-6 5', 
                    help='body part regression crop score select')                                                            


args = parser.parse_args()

#Get all cropped folders
cropped_dir = os.path.join(args.root_path, 'bpr_cropped')
if not os.path.isdir(cropped_dir):
    os.makedirs(cropped_dir)
if not os.path.isdir(os.path.join(cropped_dir, 'images')):
    os.makedirs(os.path.join(cropped_dir, 'images'))
if not os.path.isdir(os.path.join(cropped_dir, 'soft_images')):
    os.makedirs(os.path.join(cropped_dir, 'soft_images'))    
#Get information folder
txt_info_dir = os.path.join(args.root_path, 'txt_info')
if not os.path.isdir(txt_info_dir):
    os.makedirs(os.path.join(txt_info_dir, 'txt_info_dir'))  
# Downlowad BPR checkpoint
if not os.path.isfile(args.checkpoint_BPR):
    download_url(
        url="https://drive.google.com/uc?export=download&id=1UdNJNuk9fKaLoQAQ9_LzhVD4z9CL6KAg", 
        filepath=args.checkpoint_BPR
    )

Pre_bodypart = Pre_bodypart(args)
Pre_bodypart.processing()
Bodypart_regressor = Bodypart_regressor(args)
Bodypart_regressor.processing()
post_bodypart_regression = post_bodypart_regression(args)
post_bodypart_regression.processing()





