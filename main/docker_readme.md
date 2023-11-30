# Info with our current docker setup

Image is obtained from Docker's repository with tag `python:alpine3.18`

This runs a minimal linux system with `alpine` and `python 3.11.5`

The default shell is `sh`, not `bash`. 

# Execution instructions with docker

## Steps (For newcomers)

0. Install docker
1. In the root directory, run `sh build_docker_and_run.sh`. The `team_spirit` script should take over the shell session you ran that on. If you are in Windows, on a powershell terminal, type `build_docker_and_run.bat` and it should run as well.  
2. When you are done with the bot, use `Ctrl + C` to keyboard interrupt and stop the application. 
3. Run `sh clean_docker_image.sh` to clean any images that docker has created. If you are on windows, on a powershell terminal, type `clean_docker_image.bat`. 

## Steps (For those who know what they're doing)

1. Execute `docker build -t team_spirit .` in the root directory to build the image. Run this everytime that you make some changes to your code. 
2. Execute `docker run -dit --rm --name team_spirit team_spirit` to create a container out of the image. 
3. Execute `docker exec -it team_spirit sh` to get a shell session on the container. When you are done, use `exit` to get out.
4. Execute `docker stop team_spirit` to stop the container.
5. Execute `docker rmi team_spirit` to remove the image.

## Helpful commands

1. `docker image prune` to remove all dangling images. You probably want to do this periodically, to ensure that your local machine doesn't get flooded by Docker images. 
2. `docker container prune` to remove all stopped containers.
3. `docker stop [container_name]` to stop container. 
4. The `docker run` with `--rm` flag means to remove the container once the command you are running stops 

## How to retrieve logs from Docker container? 

1. Execute the script with `sh build_docker_and_run.sh`
2. When the bot didn't exit yet, connect into it by running `docker exec -it team_spirit sh`
3. Go into the `logs` directoy and view the logs produced
4. You can copy the whole logs directory by doing

## How to push a local Docker image to Docker Hub?

1. `docker login --username <username> --password <password>`. For example, I have used: `docker login --username yujiawei364557 --password highsalary`
2. Change the line in `build_docker_and_run` (corresponding to your system, modify the .sh or .bat) that says `docker build --tag team_spirit ../`, change the tag to `<username>/<repository name>`. Something like: `yujiawei364557/team_spirit`. 
3. Then, after executing `build_docker_and_run` at least once for your current version, you can call: `docker push <username>/<repository name>`, something like `docker push yujiawei364557/team_spirit`.

Note: If you plan to replace the image name into `<username>/<repository name>`, it would be better if you also replace the image name in all three of the scripts, `build_docker_and_run`, `clean_docker_image`, and `copy_logs`, as that will introduce minimum error. 