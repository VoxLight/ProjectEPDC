#!/bin/bash

# Stop all Docker containers
docker stop $(docker ps -aq)

# Remove all Docker containers
docker rm $(docker ps -aq)

# Remove all Docker images
docker rmi -f $(docker images -q)

# Remove all Docker volumes
docker volume rm VOLUME $(docker volume ls -q)