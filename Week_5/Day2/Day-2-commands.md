# Day 2 - Docker Compose and Multi Container Applications

## Start Multi Container Application

docker compose up  
docker compose up -d

## Build Containers

docker compose up --build

## Check Running Containers

docker ps

## View Container Logs

docker compose logs  
docker compose logs server

## Stop Containers

docker compose down

## Restart Containers

docker compose restart

## Execute Command Inside Container

docker compose exec backend sh

## Inspect Docker Network

docker network ls  
docker network inspect <network-name>

## Volume Inspection

docker volume ls  
docker volume inspect <volume-name>