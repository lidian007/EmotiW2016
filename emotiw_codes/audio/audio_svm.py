# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 22:11:59 2016

@author: fanyin
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 19:41:37 2016

@author: fanyin
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 20:04:39 2016

@author: fanyin
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 19 15:49:18 2016

@author: fanyin
"""

import os
import numpy as np
from sklearn import svm
import re
from pylab import * 
from sklearn.externals import joblib
feat_length = 1582
    
    

def get_feat(filename):
    lines = open(filename).readlines()
    #print len(lines)
    feat_str = lines[len(lines)-1]
    datas = re.split(',',feat_str[:-1])
    feat = np.zeros((1, feat_length))
    #print datas[1]
    for i in range(1,feat_length+1):
        feat[0, i-1] = datas[i]
    return feat
    
def get_all_feats(file_dir):    
    file_count = 0
    for fname in sorted(os.listdir(file_dir)):
        file_count += 1            
    
    feats = np.zeros((file_count, feat_length))
    count = -1
    for fname in sorted(os.listdir(file_dir)):
        count += 1
        feat = get_feat(os.path.join(file_dir, fname))
        feats[count] = feat
    return feats

test_total_dir = '../data/audio_feat'    
test_total_feats = get_all_feats(test_total_dir)
classifier = joblib.load('../models/audio_model/audio_svm.m')
audio_res = classifier.predict_proba(test_total_feats)
np.save("../audio_res.npy", audio_res)

  
