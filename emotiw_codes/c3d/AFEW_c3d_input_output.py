# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 20:16:30 2016

@author: fanyin
"""

import os
import string
import re
  
def gen_test_input_file(img_dir, txt_name, prefix):
    txt_file = open(txt_name,'w')   
    for video in os.listdir(img_dir):
        fnum = len(os.listdir(os.path.join(img_dir, video)))
        #print fnum
        count = int(fnum / 16)
        for idx in range(count):
            start_f = idx*16 + 1
            txt_file.write(prefix)
            txt_file.write(video)
            txt_file.write('/ ')
            txt_file.write(str(start_f))
            txt_file.write(' ')
            txt_file.write(str(-1))
            txt_file.write('\n')
    txt_file.close()
    
def gen_test_output_file(input_name, output_name, prefix):
    input_lines = open(input_name).readlines()
    output_file = open(output_name,'w')
    for line in input_lines:
        sp = re.split(' ', line[:-1])
        fid = sp[1]
        fid_i = int(fid)
        if fid_i < 10:
            fid_s = '00000' + fid 
        elif fid_i < 100:
            fid_s = '0000' + fid
        elif fid_i < 1000:
            fid_s = '000' + fid
        sp2 = re.split('/', sp[0])
        vid = sp2[-2]
        output_file.write(prefix  + vid + '/' + fid_s + '\n')
    output_file.close()
    
    os.mkdir(prefix)
    os.chdir(prefix)
    for line in input_lines:
        sp = re.split(' ', line[:-1])
        sp2 = re.split('/', sp[0])
        vid = sp2[-2]
        if  os.path.exists(vid):
            continue
        else:
            os.mkdir(vid)
    os.chdir('..')



#afew
img_dir = '../data/Test_afew_face_c3d'
input_name = 'Test_2016_emotion_afew_c3d_input.txt'
input_prefix = '../data/Test_afew_face_c3d/'    
gen_test_input_file(img_dir, input_name, input_prefix)
output_name = 'Test_2016_emotion_afew_c3d_output_1.txt'
output_prefix = 'output_probs_afew_1/'
gen_test_output_file(input_name, output_name, output_prefix)

output_name = 'Test_2016_emotion_afew_c3d_output_2.txt'
output_prefix = 'output_probs_afew_2/'
gen_test_output_file(input_name, output_name, output_prefix)


#qiyi
img_dir = '../data/Test_qiyi_face_c3d'
input_name = 'Test_2016_emotion_qiyi_c3d_input.txt'
input_prefix = '../data/Test_qiyi_face_c3d/'    
gen_test_input_file(img_dir, input_name, input_prefix)
output_name = 'Test_2016_emotion_qiyi_c3d_output.txt'
output_prefix = 'output_probs_qiyi/'
gen_test_output_file(input_name, output_name, output_prefix)
