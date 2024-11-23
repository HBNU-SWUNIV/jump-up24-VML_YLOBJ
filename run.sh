#!/bin/bash
docker run --detach -it --ipc=host --gpus '"device=0"' \
 -v ./ultralytics:/ultralytics \
 -v ./datasets:/content/datasets \
 ultralytics/ultralytics:latest

 # Visual Studio Code 등에서 Attach
 