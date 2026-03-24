# Day 5 - Production guide 

To run the app in production

Execute ./deploy.sh

It will run 

```
docker compose -f docker-compose.prod.yml --build -d
```

To stop the production 

```
docker compose -f docker-compose.prod.yml down
```