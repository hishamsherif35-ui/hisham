#!/bin/bash
# usage: enc.sh <input> <slug> <outdir>
IN="$1"; SLUG="$2"; OUT="$3"; T=$(mktemp -d)
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
W=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$IN")
H=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$IN")
VK=$(python3 -c "print(min(4000,int(13.4*8*1024/$DUR)-96))")
if [ $W -ge $H ]; then BIG="scale=-2:1080"; SMALL="scale=-2:720"; else BIG="scale=1080:-2"; SMALL="scale=720:-2"; fi
if [ $VK -lt 1700 ]; then VF=$SMALL; else VF=$BIG; fi
cd $T
ffmpeg -loglevel error -y -i "$IN" -vf "$VF" -c:v libx264 -preset slow -b:v ${VK}k -pass 1 -an -f null /dev/null && \
ffmpeg -loglevel error -y -i "$IN" -vf "$VF" -c:v libx264 -preset slow -b:v ${VK}k -pass 2 -profile:v high -pix_fmt yuv420p -c:a aac -b:a 96k -ac 2 -movflags +faststart "$OUT/$SLUG.mp4" && \
ffmpeg -loglevel error -y -ss $(python3 -c "print(min(6,$DUR/3))") -i "$OUT/$SLUG.mp4" -frames:v 1 -vf "scale='if(gt(iw,ih),1280,720)':-2" -q:v 4 "$OUT/$SLUG.jpg"
echo "$SLUG dur=$DUR vk=$VK vf=$VF size=$(stat -c%s "$OUT/$SLUG.mp4")"
rm -rf $T
