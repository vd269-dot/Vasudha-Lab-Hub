#!/bin/bash

echo "Hello Vasudha. Please say your phone number after the beep." | python3 -m piper --model en_US-lessac-medium.onnx --output_raw | aplay -r 22050 -f S16_LE -c 1

sleep 1

arecord -d 5 -f cd -c 1 -r 16000 number.wav

echo "Thank you. Let me transcribe that." | python3 -m piper --model en_US-lessac-medium.onnx --output_raw | aplay -r 22050 -f S16_LE -c 1

python transcribe.py number.wav --model tiny.en
