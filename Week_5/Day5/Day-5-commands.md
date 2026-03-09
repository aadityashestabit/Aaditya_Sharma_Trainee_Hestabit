# Day 5 - Production Deployment with Docker Compose

## Build and Deploy Stack

docker compose -f docker-compose.prod.yml up --build

## Deploy Using Script

./deploy.sh

## Check Running Containers

docker ps

## View Logs

docker compose -f docker-compose.prod.yml logs

## View Logs of Specific Service

docker logs backend  
docker logs frontend  
docker logs nginx

## Test Frontend

curl http://localhost:8080

## Test Backend API

curl http://localhost:8080/api

## Execute Command Inside Container

docker exec -it frontend sh  
docker exec -it backend sh

## Stop Production Stack

docker compose -f docker-compose.prod.yml down

## Debug Container Networking

docker exec -it day5-nginx-1 ping backend  
docker exec -it day5-nginx-1 ping frontend