# Day 1 - Docker Fundamentals and Linux Internals

## Check Docker Installation

docker --version  
docker version  
docker info

## Pull Base Image

docker pull node

## Build Docker Image

docker build .  
docker build -t node-app .

## Run Container

docker run \<image-id>  
docker run -p 5173:5173 \<image-id>

## List Containers

docker ps  
docker ps -a

## Enter Running Container

docker exec -it <container-id> /bin/sh

## Linux Commands Inside Container

ls  
ps  
top  
df -h

## View Container Logs

docker logs <container-id>