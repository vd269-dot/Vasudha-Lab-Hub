#!/bin/bash

echo "Hello Vasudha, welcome to Lab 3!" | python3 -m piper --model en_US-lessac-medium.onnx --output_raw | aplay -r 22050 -f S16_LE -c 1
