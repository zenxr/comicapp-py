#!/bin/bash

# stop and remove container
docker container stop comicapp-back
docker container rm comicapp-back

docker build -t comicapp-back .
# include -it --rm to run interactively
docker run -d --name comicapp-py comicapp-back
