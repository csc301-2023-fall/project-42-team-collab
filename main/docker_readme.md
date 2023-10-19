# Info with our current docker setup

Image is obtained from Docker's repository with tag `python:alpine3.18`

This runs a minimal linux system with `alpine` and `python 3.11.5`

The default shell is `sh`, not `bash`. 

# Execution instructions with docker

## Steps (For newcomers)

0. Install docker
1. In the root directory, run `sh build_docker_and_run.sh`. The `EmployedBot` script should take over the shell session you ran that on. If you are in Windows, on a powershell terminal, type `build_docker_and_run.bat` and it should run as well.  
2. When you are done with the bot, use `Ctrl + C` to keyboard interrupt and stop the application. 
3. Run `sh clean_docker_image.sh` to clean any images that docker has created.  If you are on windows, on a powershell terminal, type `clean_docker_image.bat`. 

## Steps (For those who know what they're doing)

1. Execute `docker build -t employed-bot .` in the root directory to build the image. Run this everytime that you make some changes to your code. 
2. Execute `docker run -dit --rm --name employed-bot employed-bot` to create a container out of the image. 
3. Execute `docker exec -it employed-bot sh` to get a shell session on the container. When you are done, use `exit` to get out.
4. Execute `docker stop employed-bot` to stop the container.
5. Execute `docker rmi employed-bot` to remove the image.

## Helpful commands

1. `docker image prune` to remove all dangling images.
2. `docker container prune` to remove all stopped containers.
3. `docker stop [container_name]` to stop container. 
