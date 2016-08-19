#!/bin/bash

EXPECTED_ARGS=2
E_BADARGS=65

if [ $# -lt $EXPECTED_ARGS ]
then
  echo "Usage: `basename $0` video frames/sec [size=256]"
  exit $E_BADARGS
fi

mkdir -m 755 "../data/Test_frames_data"
cd "../data/Test_frames_data"
NAME=${1%.*}
FRAMES=$2
#echo $NAME
BNAME=`basename $NAME`
echo $NAME
for video in `find $NAME -type f -name '*.avi'`
do
	echo $video
        VNAME=`echo $video | cut -d "/" -f7`
        D2NAME=`echo $VNAME | cut -d "." -f1`
	mkdir -m 755 $D2NAME
        cd $D2NAME
	ffmpeg -i $video -r $FRAMES -q:v 2 $D2NAME.%4d.jpg 
	cd ../
done
