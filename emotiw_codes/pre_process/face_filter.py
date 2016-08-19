# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 20:00:17 2016

@author: fanyin
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 10:54:34 2016

@author: fanyin
"""
import os
import numpy 
from sklearn import svm
import sys
sys.path.insert(0, '../caffe/python/')
import caffe
import time
import shutil
import string 
import re
import PIL
from PIL import Image

def face_fliter_afew(testimage_dir, save_dir):  
    prototxt = '../models/face_fliter_deploy.prototxt'
    caffemodel = '../models/face_fliter_8.caffemodel'
    caffe.set_mode_gpu()
    net = caffe.Net(prototxt, caffemodel, caffe.TEST)
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2,0,1))
    transformer.set_mean('data', numpy.load('../models/ilsvrc_2012_mean.npy').mean(1).mean(1)) # mean pixel
    transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB
  
    if os.path.exists(save_dir) == False:
        os.mkdir(save_dir)
    #counter = 0
    for subdir in sorted(os.listdir(testimage_dir)):
        cur_dir = os.path.join(testimage_dir, subdir)
        cur_save_dir = os.path.join(save_dir, subdir)
        if os.path.exists(cur_save_dir) == False:
            os.mkdir(cur_save_dir)
        face_count = 0
        for image_file in sorted(os.listdir(cur_dir)):
            if image_file[-4:] == ".jpg":
                full_dir = os.path.join(cur_dir, image_file)
                net.blobs['data'].data[...] = transformer.preprocess('data', caffe.io.load_image(full_dir))
                out = net.forward()
                #print "Predicted class is #{}.".format(out['prob'].argmax())
                #if out['prob'].argmax() == 1 and out['prob'][0,out['prob'].argmax(),0,0] >= 0.785:
                if out['prob'].argmax() == 1 and out['prob'][0,out['prob'].argmax()] >= 0.785:
                    face_count += 1
                    if face_count < 10:
                        img_rename = '00000' + str(face_count)+'.jpg'
                    elif face_count < 100:
                        img_rename = '0000' + str(face_count)+'.jpg'
                    elif face_count < 1000:
                        img_rename = '000' + str(face_count)+'.jpg'
                        #print img_rename
                    shutil.copy(full_dir, os.path.join(cur_save_dir, img_rename))
        if face_count == 0:
            os.rmdir(cur_save_dir)
        elif face_count < 16:
            print cur_dir
            for id in range(16 - face_count):
                if id + face_count + 1 <10:
                    img_add_name = '00000' + str(id + face_count + 1)+'.jpg'
                elif id + face_count + 1<100:
                    img_add_name = '0000' + str(id + face_count + 1)+'.jpg'
                shutil.copy(os.path.join(cur_save_dir, img_rename), os.path.join(cur_save_dir,img_add_name))    

def face_fliter_qiyi(testimage_dir, save_dir):  
    prototxt = '../models/face_fliter_deploy.prototxt'
    caffemodel = '../models/face_fliter_7.caffemodel'
    caffe.set_mode_gpu()
    net = caffe.Net(prototxt, caffemodel, caffe.TEST)
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2,0,1))
    transformer.set_mean('data', numpy.load('../models/ilsvrc_2012_mean.npy').mean(1).mean(1)) # mean pixel
    transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB
  
    if os.path.exists(save_dir) == False:
        os.mkdir(save_dir)
    #counter = 0
    for subdir in sorted(os.listdir(testimage_dir)):
        cur_dir = os.path.join(testimage_dir, subdir)
        cur_save_dir = os.path.join(save_dir, subdir)
        if os.path.exists(cur_save_dir) == False:
            os.mkdir(cur_save_dir)
        face_count = 0
        for image_file in sorted(os.listdir(cur_dir)):
            if image_file[-4:] == ".jpg":
                full_dir = os.path.join(cur_dir, image_file)
                net.blobs['data'].data[...] = transformer.preprocess('data', caffe.io.load_image(full_dir))
                out = net.forward()
                print "Predicted class is #{}.".format(out['prob'].argmax())
                #if out['prob'].argmax() == 1 and out['prob'][0,out['prob'].argmax(),0,0] >= 0.96:
                if out['prob'].argmax() == 1 and out['prob'][0,out['prob'].argmax()] >= 0.96:
                    face_count += 1
                    if face_count < 10:
                        img_rename = '00000' + str(face_count)+'.jpg'
                    elif face_count < 100:
                        img_rename = '0000' + str(face_count)+'.jpg'
                    elif face_count < 1000:
                        img_rename = '000' + str(face_count)+'.jpg'
                        #print img_rename
                    shutil.copy(full_dir, os.path.join(cur_save_dir, img_rename))
        if face_count == 0:
            os.rmdir(cur_save_dir)
        elif face_count < 16:
            print cur_dir
            for id in range(16 - face_count):
                if id + face_count + 1 <10:
                    img_add_name = '00000' + str(id + face_count + 1)+'.jpg'
                elif id + face_count + 1<100:
                    img_add_name = '0000' + str(id + face_count + 1)+'.jpg'
                shutil.copy(os.path.join(cur_save_dir, img_rename), os.path.join(cur_save_dir,img_add_name))  
                
                
def trans_qiyi(testimage_dir, save_dir):
    if os.path.exists(save_dir) == False:
        os.mkdir(save_dir)
    #counter = 0
    for subdir in sorted(os.listdir(testimage_dir)):
        cur_dir = os.path.join(testimage_dir, subdir)
        cur_save_dir = os.path.join(save_dir, subdir)
        if os.path.exists(cur_save_dir) == False:
            os.mkdir(cur_save_dir)
        face_count = 0
        for image_file in sorted(os.listdir(cur_dir)):
            full_dir = os.path.join(cur_dir, image_file)
            img = Image.open(full_dir)
            img = img.resize((48,48), PIL.Image.ANTIALIAS)
            img.save(full_dir)
            
            face_count += 1
            if face_count < 10:
                img_rename = 'I_100' + str(face_count)+'.jpg'
            elif face_count < 100:
                img_rename = 'I_10' + str(face_count)+'.jpg'
            elif face_count < 1000:
                img_rename = 'I_1' + str(face_count)+'.jpg'
                #print img_rename
            shutil.copy(full_dir, os.path.join(cur_save_dir, img_rename))
                
        if face_count == 0:
            os.rmdir(cur_save_dir)
        elif face_count < 16:
            print cur_dir
            for id in range(16 - face_count):
                if id + face_count + 1 <10:
                    img_add_name = 'I_100' + str(id + face_count + 1)+'.jpg'
                elif id + face_count + 1<100:
                    img_add_name = 'I_100' + str(id + face_count + 1)+'.jpg'
                shutil.copy(os.path.join(cur_save_dir, img_rename), os.path.join(cur_save_dir,img_add_name))    
                
                
testimage_dir = "../data/Test_frames_data_ali"
save_dir = "../data/Test_qiyi_face_c3d/"
face_fliter_qiyi(testimage_dir, save_dir)
save_dir_2 = "../data/Test_qiyi_face_lstm/"
trans_qiyi(save_dir, save_dir_2)
     
testimage_dir = "../data/Test_2016_Faces_Distribute"
save_dir = "../data/Test_afew_face_c3d"
face_fliter_afew(testimage_dir, save_dir)

