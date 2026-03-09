# Day 3 - NGINX Reverse Proxy and Load Balancing

## Build and Run Containers

docker compose up --build

## Start Containers in Background

docker compose up -d

## Stop Containers

docker compose down

## Check Running Containers

docker ps

## View Logs

docker logs backend1  
docker logs backend2  
docker logs nginx

## Test API Endpoint

curl http://localhost:443

## Inspect Container

docker inspect backend1

## Check Container Networking

docker network inspect \<network-name>
