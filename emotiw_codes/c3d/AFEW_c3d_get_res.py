# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 23:36:50 2016

@author: fanyin
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 12:21:50 2016

@author: fanyin
"""

import os
import numpy as np
import sys
import re
from pylab import * 

feat_length = 7

def get_feat(filename):
    lines = open(filename).readlines()
    feat_str = lines[0]
    datas = re.split(',',feat_str[:-1])
    feat = np.zeros((1, feat_length))
    for i in range(0,feat_length):
        feat[0, i] = datas[i]
    return feat
    
    
def get_c3d_prob(file_dir, video_dir, save_name):    
    num = -1
    feat_length = 7
    prediction_c3d =  np.zeros((593, feat_length))
    for fname in sorted(os.listdir(video_dir)):
            num += 1
            sp = re.split('.avi',fname)
            vid = sp[0]
            if os.path.exists(os.path.join(file_dir, vid)):
                file_count = len(os.listdir(os.path.join(file_dir, vid)))
                feats = np.zeros((file_count, feat_length))
                count = -1               
                for feat in sorted(os.listdir(os.path.join(file_dir, vid))):
                    feat = get_feat(os.path.join(file_dir, vid, feat))
                    count += 1
                    feats[count] = feat
                p_log = feats
                p_avg_log = np.mean(p_log, axis=0)
                prediction_c3d[num,:] = p_avg_log                           
    np.save(save_name,prediction_c3d)
  
test_video_dir = '../data/Test_vid_Distribute'   
  
test_prob_afew_1_dir = './output_probs_afew_1_prob/'
save_name_afew_1 = '../c3d_afew_1_res.npy'
get_c3d_prob(test_prob_afew_1_dir, test_video_dir, save_name_afew_1)

test_prob_afew_2_dir = './output_probs_afew_2_prob/'
save_name_afew_2 = '../c3d_afew_2_res.npy'
get_c3d_prob(test_prob_afew_2_dir, test_video_dir, save_name_afew_2)
     
test_prob_qiyi_dir = './output_probs_qiyi_prob/'
save_name_qiyi = '../c3d_qiyi_res.npy'
get_c3d_prob(test_prob_qiyi_dir, test_video_dir, save_name_qiyi)
