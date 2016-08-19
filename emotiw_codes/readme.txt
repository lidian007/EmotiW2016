Get AFEW6.0 test results by run the following command:
    python ./fusion.py
after running the command, a RES_txt directory is generated, the directory contains the test result for AFEW6.0 test videos, 593 test videos in total.


Also, you can extract audio and video features yourself, or test other vidoes by the following steps:

1. download data and models
   data：https://drive.google.com/open?id=0B6UurPOQfmP0TnlKTmhZUHphZ0E
   models：https://drive.google.com/open?id=0B6UurPOQfmP0R004bEdVbER1OFk
   c3d models：https://drive.google.com/open?id=0B6UurPOQfmP0U2NPUTdaN2dabzA
   
   tar zxvf data.tar.gz, place dir under root directoy, then as ./data/
   tar zxvf models1.tar.gz, place dir under root directory, then as ./models
   tar zxvf models2.tar.gz, place dir under ./c3d, then as ./c3d/models

2.audio
  1) change into the audio directory: cd ./audio
  2) get the original audio files from videos: ./extract_audio_afew.sh ../data/Test_vid_Distribute
  3) convert the format of audio files by matlab program: wav_trans.m 
  4) extactor audio features: ./extract_feat_afew.sh ../data/audio_trans_wav
  5) classify and save the audio result for emotion recognition (audio_res.npy):  python audio_svm.py

3.video
  (1) pre-processing
      1)Copy test videos and AFEW faces into the directories ./data/Test_vid_Distribute and ./data/Test_2016_Faces_Distribute separately
      2)change into the directoy: cd ./pre_process
      3) extract all frames of the videos:./extract_frames.sh ../data/Test_vid_Distribute 30
      4) face detection and alignments: ./face_detect_align ../data/Test_frames_data
      5) filtering none faces by the face filter: python face_filter.py
         after filtering none faces, the faces used in the experiments are saved at:
                      ./data/Test_afew_face_c3d
                      ./data/Test_qiyi_face_lstm
                      ./data/Test_qiyi_face_c3d  
  (2) c3d
      1) change the directory: cd ./c3d
      2) generate the input frame series by:python AFEW_c3d_input_output.py
      3) get the value of prob layer by: ./c3d_get_probs.sh
      4) data format transorm using matlab: trans_c3d_binary_prob.m
      5) save the emotion classification result in npy format by:  python AFEW_c3d_get_res.py

  (3) CNN-RNN
      1) cd ./lstm
      2) run the command: python classify_vgg_fy.py

4. get the final result
   run in the command: python fusion.py
   the video results are saved in the directory of RES_txt

----------------------

requirments
ffpemg 
caffe
python 2.7
matlab 2015
