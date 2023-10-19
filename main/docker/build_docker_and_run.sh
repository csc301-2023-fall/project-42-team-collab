#!/bin/bash

echo 'Building docker image using dockerfile...'
docker build --tag test_main .

docker run --rm -it --name test_main test_main python ./main.py
