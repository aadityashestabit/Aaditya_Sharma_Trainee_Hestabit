#!/bin/bash

echo "Starting production containers..."

docker compose -f docker-compose.prod.yml up -d --build
