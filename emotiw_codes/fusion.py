# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 23:58:09 2016

@author: fanyin
"""
import os
import numpy as np
import re 

edict = {}
edict[0] = 'Angry'
edict[1] = 'Disgust'
edict[2] = 'Fear'
edict[3] = 'Happy'
edict[4] = 'Neutral'
edict[5] = 'Sad'
edict[6] = 'Surprise'

def compute_fusion(pred_1, pred_2, pred_3,pred_4, pred_5, p1, p2,p3, p4):
    fusion_pred = p1*pred_1 + p2*pred_2 + p3*pred_3 + p4*pred_4 + (1-p1-p2-p3-p4)*pred_5
    return fusion_pred 
    
def dict_vid_count():
    vid_arr = []
    fp_list = open('./data/vid_list.txt', 'r')
    while 1:
    #for vname in sorted(os.listdir('/home/fanyin/emotiow_codes_bak/data/Test_vid_Distribute/')):
        #sp = re.split('.avi',vname)
        #vid = sp[0]
        vid = fp_list.readline()
        if not vid:
           fp_list.close()
           return vid_arr
        vid_arr.append(vid[:-1])
        #vidl = vid + '\n'
        #fp_list.write(vidl)
    fp_list.close()
    return vid_arr

    
def gen_res_files(pred, vid_arr):
    save_dir = './RES_txt'
    os.mkdir(save_dir)
    for i in range(593):
        label = pred[i]
        vid = vid_arr[i]
        save_name = str(vid) + '.txt'
        fp = open(os.path.join(save_dir, save_name), 'w')
        fp.write(edict[label])
        fp.close()   
    
vid_arr = dict_vid_count()    
audio_res = np.load('./audio_res.npy')
c3d_qiyi_res = np.load('./c3d_qiyi_res.npy')
c3d_afew_1_res = np.load('./c3d_afew_1_res.npy')
c3d_afew_2_res = np.load('./c3d_afew_2_res.npy')
lstm_res = np.load('./lstm_res.npy')
pred_p = compute_fusion(c3d_qiyi_res, c3d_afew_2_res,lstm_res,c3d_afew_1_res, audio_res ,0.05,0.15,0.25,0.03)
pred_l = np.argmax(pred_p ,1)
#audio_res_bak = np.load('./audio_res_bak.npy')
#pred_p = compute_fusion(c3d_qiyi_res, c3d_afew_2_res,lstm_res,c3d_afew_1_res, audio_res_bak ,0.05,0.15,0.26,0.02)
pred_l = np.argmax(pred_p ,1)
gen_res_files(pred_l, vid_arr)
