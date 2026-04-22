# Week 4

# Day 1 — Backend System Bootstrapping & Lifecycle

This document describes how I designed and implemented the **backend system initialization architecture** using Node.js and Express.

The goal of this setup was to build a backend that is:

- Structured
- Environment-driven
- Production ready
- Easy to debug
- Scalable

---

# Learning Objectives

The main focus areas for this implementation were:

- Understanding the **Node.js runtime lifecycle**
- Implementing **environment-driven configuration**
- Creating a **controlled application startup**
- Implementing **graceful shutdown**
- Structuring a **production-level backend architecture**

---

# Project Folder Structure

The backend follows a strict modular architecture with clearly separated responsibilities.

```
src/
│
├── config/
│   └── index.js
│
├── loaders/
│   ├── app.js
│   └── db.js
│
├── models/
│
├── routes/
│
├── controllers/
│
├── services/
│
├── repositories/
│
├── middlewares/
│
├── utils/
│   └── logger.js
│
├── jobs/
│
├── logs/
│
└── server.js
```

### Folder Responsibilities

| Folder | Responsibility |
|------|------|
| config | Environment configuration loader |
| loaders | Initializes application subsystems |
| models | Database schemas |
| routes | API endpoint definitions |
| controllers | Request/response logic |
| services | Business logic |
| repositories | Database queries |
| middlewares | Express middlewares |
| utils | Utility modules such as logger |
| jobs | Background jobs / workers |
| logs | Application logs |

---

# Node.js Runtime Lifecycle

Understanding the Node.js runtime lifecycle helps in designing predictable backend startup behavior.

```
Process Start
     │
     ▼
Environment Variables Loaded
     │
     ▼
Configuration Initialized
     │
     ▼
Logger Initialized
     │
     ▼
Database Connection
     │
     ▼
Express App Bootstrapped
     │
     ▼
Middlewares Registered
     │
     ▼
Routes Mounted
     │
     ▼
Server Listening
     │
     ▼
Runtime Event Loop
     │
     ▼
Graceful Shutdown
```

---

# Node.js Event Loop Phases

The Node.js event loop processes asynchronous operations in multiple phases.

```
┌───────────────────────────┐
│ Timers                    │
│ setTimeout / setInterval  │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│ Pending Callbacks         │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│ Idle / Prepare            │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│ Poll Phase (I/O)          │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│ Check Phase               │
│ setImmediate()            │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│ Close Callbacks           │
└───────────────────────────┘
```

---

# Environment Driven Configuration

The backend supports multiple environments.

Supported configuration files:

```
.env.local
.env.dev
.env.prod
```

Each environment can define its own configuration values.

Example `.env.dev`

```
PORT=4000
DB_URI=mongodb://localhost:27017/dev-db
```

# Logger Setup

Logging is handled using **Winston**.

File:
```
src/utils/logger.js
```

### Example Startup Logs

```
✔ Server started on port 4000
✔ Database connected
✔ Middlewares loaded
```

Logs are stored inside the `logs/` directory.

---

# Database Loader

Database initialization is handled separately to keep the architecture modular.

File:

```
src/loaders/db.js
```

---

# Express Application Loader

The Express app initialization is isolated into its own loader.

File:

```
src/loaders/app.js
```

Responsibilities:

- Initialize Express
- Register middlewares
- Mount routes
- Attach error handlers



---

# Dependency Orchestration

Each component of the system initializes in a controlled order.

```
Configuration
     │
     ▼
Logger
     │
     ▼
Database Connection
     │
     ▼
Express Application
     │
     ▼
Middlewares
     │
     ▼
Routes
     │
     ▼
Server Listening
```

This ensures the backend starts in a predictable and safe manner.

---

# Backend Request Flow

```
Client
   │
   ▼
Routes
   │
   ▼
Controller
   │
   ▼
Service Layer
   │
   ▼
Repository Layer
   │
   ▼
Database
```

### Layer Responsibilities

| Layer | Responsibility |
|------|------|
| Routes | Define API endpoints |
| Controller | Handle request/response |
| Service | Business logic |
| Repository | Database interaction |
| Model | Schema definition |

---

# Node Clustering Concept

By default Node.js runs on a single CPU core.

To utilize multiple cores, clustering can be used.


---

# Graceful Shutdown

Production applications must shutdown safely to avoid corrupted processes.

Signals triggering shutdown:

```
SIGINT
SIGTERM
```

Graceful shutdown ensures:

- Open requests complete
- Database connections close safely
- Resources are released

---

# Expected Startup Logs

When the backend starts successfully the logs should look similar to:

```
[INFO] Environment loaded: dev
[INFO] Database connected
[INFO] Middlewares loaded
[INFO] Routes mounted: 23 endpoints
[INFO] Server started on port 4000
```

These logs make debugging deployment issues significantly easier.

---

# Deliverables

The core deliverables for this backend system include:

```
src/loaders/app.js
src/loaders/db.js
src/utils/logger.js
```

These files form the **core system responsible for initializing the backend application**.

---

# Summary

By implementing this architecture I created a backend system that includes:

- Structured folder architecture
- Environment-based configuration
- Modular loader pattern
- Centralized logging
- Dependency orchestration
- Controlled application startup
- Graceful shutdown support

This setup forms a **strong foundation for building scalable and production-ready Node.js applications**.

---

# Day 2 — Data Design & Query Performance (Non-CRUD)

This document explains how I designed the **data layer of the backend system** with a focus on **query performance and scalable schema design**.

The goal of this step was to build a database structure that performs well for **read-heavy workloads**, which is common in most production systems.

---

# Learning Objectives

During this implementation I focused on understanding:

- Schema design for **read-heavy systems**
- **Query cost analysis**
- **Data lifecycle management**
- Efficient **indexing strategies**
- Pagination patterns for scalable APIs
- Implementing the **Repository Pattern**

---

# Folder Structure

The data layer components are organized into **models and repositories**.

```
src/
│
├── models/
│   ├── User.model.js
│   └── Product.model.js
│
├── repositories/
│   ├── user.repository.js
│   └── product.repository.js
```

### Responsibility Breakdown

| Layer | Responsibility |
|------|------|
Models | Define database schema |
Repositories | Handle database queries |
Services | Business logic |
Controllers | Request/response |

---

# Database Architecture Flow

```
Client
   │
   ▼
Controller
   │
   ▼
Service
   │
   ▼
Repository
   │
   ▼
MongoDB
```

Repositories isolate **database logic from business logic**, making the system easier to test and maintain.

---


# Data Lifecycle Rules

Data lifecycle determines **how long documents live and when they should be deleted automatically**.

MongoDB supports this using **TTL indexes**.

Example:

```
Session
   │
   ├── userId
   ├── token
   └── expiresAt
```

TTL index automatically removes expired documents.



---

# Indexing Strategy

Indexes dramatically improve query performance.

### Compound Index

Used when queries filter using multiple fields.

Example:

```
{ status: 1, createdAt: -1 }
```

This optimizes queries like:

```
find orders by status sorted by newest
```

---

### Sparse Index

Sparse indexes only include documents that contain the indexed field.

Useful when some documents **do not contain optional fields**.

---

# Pagination Strategies

Pagination becomes expensive when datasets grow large.

Two main strategies exist.

---

## Offset Pagination (skip / limit)

```
GET /orders?page=3&limit=10
```

### Problem

Large offsets cause **slow queries**.

---

## Cursor Pagination (Preferred)

Uses the last record as a cursor.

```
GET /orders?cursor=65e0a12
```


### Benefits

- Faster queries
- Better scalability
- Works well with indexes

---

# User Schema

File:

```
src/models/User.model.js
```

---

# Deliverables

The final implementation includes:

```
src/models/user.model.js
src/models/product.model.js

src/repositories/user.repository.js
src/repositories/product.repository.js
```
---

# Day 3 — Query Pipelines & Failure-Safe APIs

The focus of this phase was **handling complex query behavior while ensuring predictable API responses and safe failure handling**.

Instead of building simple CRUD endpoints, the APIs were designed to support:

- dynamic filters
- search
- sorting
- pagination - cursor based
- soft deletion
- standardized error handling

The goal was to make the API **robust, flexible, and production-ready**.

---

# Learning Objectives

During this implementation I focused on:

- API behavior under **complex filtering conditions**
- Designing **dynamic query pipelines**
- Implementing **controlled soft deletion**
- Creating **unified error contracts**
- Structuring the backend using **Controller → Service → Repository architecture**

---

# Folder Structure

The core components introduced during this phase are controllers, services, and global middleware.

```
src/
│
├── controllers/
│   └── product.controller.js
│
├── services/
│   └── product.service.js
│
├── middlewares/
│   └── error.middleware.js
```

### Layer Responsibilities

| Layer | Responsibility |
|------|------|
Controllers | Handle HTTP requests and responses |
Services | Business logic and query building |
Repositories | Database access layer |
Middlewares | Cross-cutting concerns like error handling |

---

# API Architecture Flow

The backend follows a **layered architecture** to separate responsibilities.

```
Client
   │
   ▼
Routes
   │
   ▼
Controller
   │
   ▼
Service
   │
   ▼
Repository
   │
   ▼
Database
```


---

# Query Pipeline Architecture

Instead of writing separate endpoints for every filter combination, a **dynamic query pipeline** is constructed based on request parameters.

```
Incoming Request
      │
      ▼
Parse Query Parameters
      │
      ▼
Build Dynamic Filters
      │
      ▼
Apply Sorting
      │
      ▼
Apply Pagination
      │
      ▼
Execute Query
      │
      ▼
Return Response
```

This approach allows a **single endpoint** to support many query combinations.

---

# Example Complex Query

Example request:

```
GET /products?search=phone&minPrice=100&maxPrice=500&sort=price:desc&tags=apple,samsung
```

This request can include multiple filtering conditions simultaneously.

### Query Components

| Parameter | Purpose |
|------|------|
search | text search across product fields |
minPrice | lower price bound |
maxPrice | upper price bound |
sort | sorting order |

---


# Soft Delete Architecture

Instead of permanently deleting records, **soft deletion** marks records as deleted.

This preserves historical data and prevents accidental data loss.

### Soft Delete Fields

```
isdeleted
deletedAt
```

When a delete operation occurs:

```
DELETE api/products/:id
```

The product is **not removed from the database**.

Instead:

```
deleted = true
deletedAt = timestamp
```

---

# Soft Delete Lifecycle

```
Delete Request
      │
      ▼
Mark Document as Deleted
      │
      ▼
Set deletedAt timestamp
      │
      ▼
Exclude from default queries
```

Default queries automatically exclude deleted items.

However, the API allows retrieving deleted records when needed.

This makes the system safer and supports **auditability**.

---

# Failure-Safe API Design

Production APIs must handle failures gracefully.

The system uses **centralized error handling** with structured responses.

Instead of returning inconsistent errors, all failures follow a **standard error contract**.

---

# Unified Error Response Format

All errors follow this format:

```
{
  success: false,
  message: "Error description",
  code: "ERROR_CODE",
  timestamp: "ISO timestamp",
  path: "/api/products"
}
```

### Field Description

| Field | Purpose |
|------|------|
success | indicates failure |
message | human readable error |
code | machine readable error code |
timestamp | time of error |
path | endpoint where error occurred |

---

# Error Handling Architecture

Errors are handled through a centralized middleware.

```
Controller
     │
     ▼
Throw Error
     │
     ▼
Error Middleware
     │
     ▼
Standard Error Response
```

Benefits:

- consistent API responses
- easier debugging
- simplified error handling in controllers

---

# Typed Errors

Instead of generic errors, the system uses **typed errors**.

Examples include:

```
ValidationError
NotFoundError
AuthenticationError
AuthorizationError
DatabaseError
```

Each error type maps to a specific **error code and HTTP status**.

Example mapping:

```
ValidationError → 400
NotFoundError → 404
AuthenticationError → 401
InternalError → 500
```

---

# Deliverables

The implementation produced the following files.

```
src/controllers/product.controller.js
src/services/product.service.js
src/middlewares/error.middleware.js
```

# Day 4 — API Defense & Input Control

# Learning Objectives

During this implementation I focused on:

- Reducing the **API attack surface**
- Implementing **strict request validation**
- Enforcing **payload whitelisting**
- Protecting APIs from **injection attacks**
- Implementing **rate limiting**
- Applying **HTTP security headers**
- Sanitizing incoming query parameters

---

# Folder Structure

The security layer was implemented using centralized middleware components.

```
src/
│
├── middlewares/
│   ├── validate.js
│   └── security.js
```

### Responsibility Breakdown

| Component | Responsibility |
|----------|---------------|
validate middleware | Request schema validation |
security middleware | Global security protections |
controllers | Business logic |
services | Application logic |

---

# API Security Architecture

Security protections are applied **before the request reaches the business logic**.

```
Client Request
      │
      ▼
Security Middleware
      │
      ▼
Rate Limiting
      │
      ▼
Input Sanitization
      │
      ▼
Validation Middleware
      │
      ▼
Controller
      │
      ▼
Service
      │
      ▼
Database
```

This ensures malicious requests are **blocked early in the request lifecycle**.

---

# Mandatory Security Protections

The system enforces the following protections globally.

### Payload Whitelisting

Only allowed fields are accepted in requests.

```
Incoming Payload
     │
     ▼
Allowed Fields Filtered
     │
     ▼
Unknown Fields Removed
```

This prevents attackers from sending **unexpected parameters**.

---

### Schema-Level Validation

All requests must match predefined schemas.

```
Request Payload
     │
     ▼
Validation Schema
     │
     ▼
Valid Request → Continue
Invalid Request → Reject
```

Validation is applied to:

- request body
- query parameters
- route parameters

---

### Header Hardening

Security headers are applied to protect browsers and clients.

```
Client Request
     │
     ▼
Server Response
     │
     ▼
Security Headers Added
```


---

### Query Sanitization

Query parameters are sanitized to prevent malicious injections.

```
Incoming Query
     │
     ▼
Sanitization Layer
     │
     ▼
Clean Query Object
```

This protects the database from **malformed or dangerous query structures**.

---

# Common Attacks Prevented

The system specifically protects against several common web vulnerabilities.

---

# NoSQL Injection

NoSQL injection occurs when attackers inject query operators into database queries.

Example attack idea:

```
{ email: { "$ne": null } }
```

Protection strategy:

```
Incoming Query
     │
     ▼
Sanitization
     │
     ▼
Operator Filtering
     │
     ▼
Safe Database Query
```

---

# Cross-Site Scripting (XSS)

XSS occurs when malicious scripts are injected into responses.

Example attack:

```
<script>alert("attack")</script>
```

Protection strategy:

```
User Input
     │
     ▼
Sanitization
     │
     ▼
Escaped Output
```

This prevents malicious scripts from executing in browsers.

---


# Validation Layer

Validation schemas enforce **strict input rules**.

Validation occurs before the controller executes.

```
Request
   │
   ▼
Validation Middleware
   │
   ├── Valid Input → Continue
   └── Invalid Input → Reject
```

Schemas were designed for:

- User input validation
- Product data validation
- Query parameter validation

This prevents invalid data from entering the system.

---

# Global Security Middleware

All security protections are centralized in one middleware layer.

```
Application Startup
      │
      ▼
Security Middleware Registered
      │
      ▼
Every Request Passes Through
```

Protections applied globally include:

- security headers
- CORS policy
- request throttling
- payload size limits

---

# Deliverables

The following components were implemented.

```
src/middlewares/validate.js
src/middlewares/security.js
```

---

# Day 5 — Async Workers, Observability & Release Readiness


# Learning Objectives

During this stage I focused on:

- implementing **asynchronous job workers**
- designing **queue-based task processing**
- building **structured logging pipelines**
- implementing **request tracing**

---

# Folder Structure

The following components were introduced for asynchronous processing and observability.

```
src/
│
├── jobs/
│   └── email.job.js
│
├── utils/
│   └── tracing.js
│
├── logs/
│   └── *.log
│
prod/
│
├── ecosystem.config.js
└── .env.example
```

Additional deliverables include:

```
Postman Collection Export
DEPLOYMENT-NOTES.md
```

---

# Background Job Architecture

Certain tasks should **not run inside the request-response lifecycle**, especially tasks that are slow or resource-heavy.

Examples include:

- sending emails
- generating reports
- exporting files
- processing uploads

To handle such tasks efficiently, a **job queue architecture** was implemented.

```
Client Request
      │
      ▼
API Server
      │
      ▼
Job Added To Queue
      │
      ▼
Redis Queue
      │
      ▼
Worker Process
      │
      ▼
Job Execution
      │
      ▼
Logs / Result
```

This allows the API to respond quickly while work is handled asynchronously.

---

# Queue System Design

A queue system ensures jobs are **executed reliably and sequentially**.

```
Producer (API Server)
        │
        ▼
      Queue
        │
        ▼
     Worker
        │
        ▼
   Job Processor
```

### Key Components

| Component | Role |
|----------|------|
Producer | Adds jobs to queue |
Queue | Stores pending tasks |
Worker | Processes tasks |
Redis | Queue storage backend |

If Redis is unavailable, the system can fallback to **in-memory job processing**.

---

# Job Lifecycle

Each job follows a lifecycle from creation to completion.

```
Job Created
     │
     ▼
Queued
     │
     ▼
Picked by Worker
     │
     ▼
Processing
     │
     ▼
Completed / Failed
```

If a job fails, it does not immediately terminate.

Instead it uses **retry and backoff strategies**.

---

# Retry & Backoff Strategy

Retries ensure temporary failures do not permanently break job execution.

```
Job Failure
     │
     ▼
Retry Scheduled
     │
     ▼
Backoff Delay Applied
     │
     ▼
Worker Retries Job
```

Backoff strategies prevent excessive retry attempts and reduce system load.

---

# Worker Process Architecture
Workers run as **separate processes** from the main API server.

```
API Server
     │
     ▼
Adds Job To Queue
     │
     ▼
Redis Queue
     │
     ▼
Worker Process
     │
     ▼
Execute Job
```

Separating workers improves system stability because heavy tasks **do not block API performance**.

---

# Observability

Observability allows engineers to **understand what is happening inside the system**.

The backend implements observability through:

- structured logging
- request tracing
- correlation IDs
- job execution logs

```
Application Events
        │
        ▼
Structured Logs
        │
        ▼
Log Files
        │
        ▼
Monitoring / Debugging
```

---

# Structured Logging

Logs are recorded in a structured format to make them easier to analyze.

```
Application Event
     │
     ▼
Structured Log Entry
     │
     ▼
Log File
```

Logs include information such as:

- request ID
- timestamp
- service name
- log level
- message

Example log categories:

```
info
warn
error
debug
```

Logs are stored in the `logs/` directory.

---

# Request Tracing

Request tracing allows tracking a request across the entire backend.

Each request is assigned a **unique identifier**.

```
Incoming Request
       │
       ▼
Generate Request ID
       │
       ▼
Attach To Request Context
       │
       ▼
Include In Logs
```

Example request header:

```
X-Request-ID
```

---



# Postman Collection

A complete **Postman collection** was created to allow developers to test the API easily.

The collection includes:

- grouped endpoints
- environment variables
- example requests
- sample responses

```
Postman Workspace
      │
      ▼
Collection
      │
      ▼
Folders (Users / Products / Orders)
      │
      ▼
Requests
```

Environment variables were configured for:

```
base_url
auth_token
environment
```

---

# Production Deployment Preparation

To make the backend deployment-ready, a **production configuration folder** was introduced.

```
prod/
│
├── ecosystem.config.js
└── .env.example
```

---

# Process Manager (PM2)

PM2 is used to manage backend processes in production.

```
PM2
 │
 ▼
Start Application
 │
 ▼
Monitor Processes
 │
 ▼
Restart On Failure
```

Benefits of using PM2:

- automatic restarts
- process monitoring
- cluster mode support
- log management

---

# Environment Configuration

An example environment file was created for deployment.

```
.env.example
```

This file documents required environment variables without exposing secrets.

Example categories include:

- database configuration
- API port
- Redis connection
- logging configuration

---

# Deliverables

The following components were implemented during this phase.

```
src/jobs/email.job.js
src/utils/tracing.js
```

Documentation and deployment artifacts:

```
Postman Collection Export
DEPLOYMENT-NOTES.md
```

Production configuration:

```
prod/ecosystem.config.js
prod/.env.example
```

---