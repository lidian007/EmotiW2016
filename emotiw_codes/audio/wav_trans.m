first_dir = '../data/audio_ori_wav/';
save_dir = '../data/audio_trans_wav/';
mkdir(save_dir)
subdirs =  dir(first_dir);
for i = 3 : length(subdirs)
    strcat(first_dir,subdirs(i).name)
    audioinfo(strcat(first_dir,subdirs(i).name))
    [y, FS]=audioread(strcat(first_dir,subdirs(i).name));
    audiowrite(strcat(save_dir,subdirs(i).name),y,FS);
end