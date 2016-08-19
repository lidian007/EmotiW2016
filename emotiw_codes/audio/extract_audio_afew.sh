#!/bin/bash

EXPECTED_ARGS=1
E_BADARGS=65

if [ $# -lt $EXPECTED_ARGS ]
then
  echo "Usage: `basename $0`"
  exit $E_BADARGS
fi

#if [ ! -d "data"]; then
#  mkdir -m 755 "data"
#fi

mkdir -m 755 "../data/audio_ori_wav"
cd "../data/audio_ori_wav"
NAME=${1%.*}
BNAME=`basename $NAME`
for video in `find $NAME -type f -name '*.avi'`
do
	echo $video
        VNAME=`echo $video | cut -d "/" -f7`
        #if [ ! -d "$D1NAME"]; then
        D2NAME=`echo $VNAME | cut -d "." -f1`
        echo $D2NAME
        ffmpeg -i $video -vn -acodec copy $D2NAME.wav
done
