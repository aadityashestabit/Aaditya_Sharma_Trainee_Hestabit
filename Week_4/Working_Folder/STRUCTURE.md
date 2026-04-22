# Week 4 - BACKEND SYSTEMS & PRODUCTION ENGINEERING

## Week 4 - Folder Structure

```
.
├── node_modules
├── src
│   ├── config
│   │   ├── index.js
│   │   └── redis.js
│   │
│   ├── controllers
│   │   ├── product.controller.js
│   │   └── user.controller.js
│   │
│   ├── jobs
│   │   └── email.job.js
│   │
│   ├── loaders
│   │   ├── app.js
│   │   └── db.js
│   │
│   ├── logs
│   │   ├── combined.log
│   │   └── error.log
│   │
│   ├── middlewares
│   │   ├── auth.middleware.js
│   │   ├── error.middleware.js
│   │   ├── role.middleware.js
│   │   ├── security.js
│   │   └── validate.js
│   │
│   ├── models
│   │   ├── product.model.js
│   │   └── user.model.js
│   │
│   ├── repositories
│   │   ├── product.repository.js
│   │   └── user.repository.js
│   │
│   ├── routes
│   │   ├── email.routes.js
│   │   ├── product.routes.js
│   │   └── user.routes.js
│   │
│   ├── seeders
│   │   ├── product.seeder.js
│   │   └── user.seeder.js
│   │
│   ├── services
│   │   ├── product.service.js
│   │   └── user.service.js
│   │
│   ├── utils
│   │   ├── AppError.js
│   │   ├── cursor.js
│   │   ├── logger.js
│   │   └── tracing.js
│   │
│   ├── validators
│   │   ├── product.schema.js
│   │   └── user.schema.js
│   │
│   ├── workers
│   │   └── email.worker.js
│   │
│   └── prod
│       ├── ecosystem.config.js
│       └── env.example
│
├── .env.dev
├── .env.local
├── .env.prod
├── .gitignore
├── NodeJs-Backend.postman_collection.json
├── package-lock.json
├── package.json
└── server.js
```