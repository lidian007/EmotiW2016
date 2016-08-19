# -*- coding: utf-8 -*-
"""
Created on Fri May 20 18:34:56 2016

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
import sys
import string
import re
from pylab import * 
import glob
caffe_root = '../../'
import sys
sys.path.insert(0,caffe_root + 'python')
import caffe
caffe.set_mode_gpu()
caffe.set_device(1)

feat_length = 1582

def lstm_classify_video(frames, net, transformer, is_flow):
  clip_length = 16
  offset = 8
  input_images = []
  for im in frames:
    input_im = caffe.io.load_image(im)
    if (input_im.shape[0] != 256 or input_im.shape[1] != 256):
      input_im = caffe.io.resize_image(input_im, (256,256))
    input_images.append(input_im)
  vid_length = len(input_images)
  input_data = []
  for i in range(0,vid_length,offset):
    if (i + clip_length) < vid_length:
      input_data.extend(input_images[i:i+clip_length])
    else:  #video may not be divisible by clip_length
      input_data.extend(input_images[-clip_length:])
  output_predictions = np.zeros((len(input_data),7))
  for i in range(0,len(input_data),clip_length):
    clip_input = input_data[i:i+clip_length]
    clip_input = caffe.io.oversample(clip_input,[224,224])
    clip_clip_markers = np.ones((clip_input.shape[0],1,1,1))
    clip_clip_markers[0:10,:,:,:] = 0
#    if is_flow:  #need to negate the values when mirroring
#      clip_input[5:,:,:,0] = 1 - clip_input[5:,:,:,0]
    caffe_in = np.zeros(np.array(clip_input.shape)[[0,3,1,2]], dtype=np.float32)
    for ix, inputs in enumerate(clip_input):
      caffe_in[ix] = transformer.preprocess('data',inputs)
    out = net.forward_all(data=caffe_in, clip_markers=np.array(clip_clip_markers))
    output_predictions[i:i+clip_length] = np.mean(out['probs'],1)
  print np.mean(output_predictions,0).argmax(), np.mean(output_predictions,0)
  return np.mean(output_predictions,0).argmax(), output_predictions

def initialize_transformer(is_flow):
  shape = (10*16, 3, 224, 224)
  transformer = caffe.io.Transformer({'data': shape})
  channel_mean = np.zeros((3,224,224))
  if is_flow == False:
    image_mean = [104.00699, 116.66877, 122.67892]
    for channel_index, mean_val in enumerate(image_mean):
        channel_mean[channel_index, ...] = mean_val
    transformer.set_mean('data', channel_mean)
    #transformer.set_mean('data', np.load('imagenet_mean.npy').mean(1).mean(1))
  else:
    mean_flow = np.zeros((3,1,1))
    mean_flow[:,:,:] = 128
    for channel_index, mean_val in enumerate(mean_flow):
      channel_mean[channel_index, ...] = mean_val
      transformer.set_mean('data', channel_mean)

  transformer.set_raw_scale('data', 255)
  transformer.set_channel_swap('data', (2, 1, 0))
  transformer.set_transpose('data', (2, 0, 1))
  transformer.set_is_flow('data', is_flow)
  return transformer



def get_video_res():
    transformer_RGB = initialize_transformer(False)
    lstm_model = 'deploy_lstm_vgg.prototxt'
    RGB_lstm = 'emotion_lstm.caffemodel'
    RGB_lstm_net =  caffe.Net(lstm_model, RGB_lstm, caffe.TEST)
    val_face_dir = '../data/Test_qiyi_face_lstm'

    val_video_dir = './Test_videos/Test_vid_Distribute'

    lcount = 0
    for ename in sorted(os.listdir(val_video_dir)):
        lcount += 1
    print lcount
    
    prediction_video = np.zeros((lcount,7))
    count = 0
    for vname in sorted(os.listdir(val_video_dir)):
        sp = re.split('.avi',vname)
        video = sp[0]
        print count,video
        if os.path.exists(os.path.join(val_face_dir, video)):
            RGB_frames = glob.glob('%s/%s/*.jpg' %(val_face_dir, video))
            class_RGB_lstm, predictions_RGB_lstm = lstm_classify_video(RGB_frames, RGB_lstm_net, transformer_RGB, False) 
            prediction_video[count,:] = np.mean(predictions_RGB_lstm,0)
        count += 1
    del RGB_lstm_net
    np.save('lstm_res.npy',prediction_video)
    return prediction_video


video_pred = get_video_res()

    
