#!/bin/bash

echo 'Building docker image using dockerfile...'
docker build --tag employed-bot .

docker run --rm -it --name employed-bot employed-bot python ./main/EmployedBot.py
