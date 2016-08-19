#!/bin/bash

EXPECTED_ARGS=1
E_BADARGS=65

if [ $# -lt $EXPECTED_ARGS ]
then
  echo "Usage: `basename $0` video frames/sec [size=256]"
  exit $E_BADARGS
fi

#if [ ! -d "data"]; then
#  mkdir -m 755 "data"
#fi

mkdir -m 755 "../data/audio_feat"
cd "../data/audio_feat"
NAME=${1%.*}
BNAME=`basename $NAME`
echo $BNAME
for video in `find $NAME -type f -name '*.wav'`
do
	echo $video
        VNAME=`echo $video | cut -d "/" -f7`
        D2NAME=`echo $VNAME | cut -d "." -f1`
        #if [ ! -d "$D1NAME"]; then
  	#  mkdir -m 755 $D1NAME
        #fi
#        ../../SMILExtract -C ../../config/IS12_speaker_trait.conf -I $video -O $D2NAME.audio_feat.txt
        ../../audio/SMILExtract -C ../../audio/emobase2010.conf -I $video -O $D2NAME.audio_feat.txt
#	ffmpeg -i $video -r $FRAMES $D2NAME.%4d.jpg 
done
rm smile.log
