#!/bin/bash

echo 'Building docker image using dockerfile...'
docker build --tag team_spirit ../
docker run --rm -it --name team_spirit team_spirit python main.py
