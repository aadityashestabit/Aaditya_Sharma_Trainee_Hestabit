# ARCHITECTURE.md

## Overview

This document describes the overall architecture of the Week 4 backend system — a production-ready Node.js and Express application built with a strong emphasis on modularity, security, observability, and async processing.

The system was designed from the ground up to be environment-driven, meaning it can run cleanly across local development, staging, and production environments without code changes. Every layer of the application has a single, clearly defined responsibility, and the startup sequence is deterministic so that failures are easy to trace and fix.

---

## Folder Structure

```
src/
├── config/
│   └── index.js            
│
├── loaders/
│   ├── app.js               
│   └── db.js                
│
├── models/
│   ├── User.model.js
│   └── Product.model.js
│
├── routes/                   
│
├── controllers/
│   └── product.controller.js
│
├── services/
│   └── product.service.js
│
├── repositories/
│   ├── user.repository.js
│   └── product.repository.js
│
├── middlewares/
│   ├── validate.js           
│   ├── security.js           
│   └── error.middleware.js   
│
├── utils/
│   ├── logger.js             
│   └── tracing.js            
│
├── jobs/
│   └── email.job.js          
│
└── logs/                    

prod/
├── ecosystem.config.js       
└── .env.example            
```

---

## Application Startup Lifecycle

When the server starts, every subsystem initializes in a strict, predictable order. This matters because if the database hasn't connected yet when the first request arrives, things break in confusing ways. By controlling the boot sequence explicitly, failures surface early and clearly.

```
┌─────────────────────────────────────┐
│         Process Start               │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│     Environment Variables Loaded    │
│     (.env.local / .env.dev /        │
│      .env.prod)                     │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│     Configuration Initialized       │
│     (src/config/index.js)           │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│     Logger Initialized              │
│     (Winston — src/utils/logger.js) │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│     Database Connected              │
│     (src/loaders/db.js)             │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│     Express App Bootstrapped        │
│     (src/loaders/app.js)            │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│     Middlewares Registered          │
│     (security, validation, tracing) │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│     Routes Mounted                  │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│     Server Listening on Port        │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│     Runtime Event Loop              │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│     Graceful Shutdown               │
│     (SIGINT / SIGTERM)              │
└─────────────────────────────────────┘
```

A successful startup produces logs that look like this:

```
[INFO] Environment loaded: dev
[INFO] Database connected
[INFO] Middlewares loaded
[INFO] Routes mounted: 23 endpoints
[INFO] Server started on port 4000
```

---

## Request Flow

Once the server is running, every incoming HTTP request travels through a layered stack. Each layer has one job and passes control to the next.

```
         Client
           │
           ▼
  ┌─────────────────┐
  │  Security Layer │  ← rate limiting, headers, CORS, payload limits
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │   Validation    │  ← schema validation, input sanitization
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │   Controller    │  ← parse request, call service, send response
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │    Service      │  ← business logic, query pipeline construction
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │   Repository    │  ← database queries only, no business logic here
  └────────┬────────┘
           │
           ▼
         MongoDB
```

The reason for this separation is maintainability. If you need to change how data is fetched from the database, you only touch the repository. If you need to change a business rule, you only touch the service. Controllers stay thin and focused purely on HTTP concerns.

---

## Security Architecture

All incoming requests pass through a security layer before they ever reach business logic. This means malicious or malformed requests are rejected as early as possible, and the controllers never have to worry about defending themselves.

The security layer handles four main things:

**Payload whitelisting** strips any fields from the request body that are not explicitly allowed. This prevents attackers from injecting unexpected parameters that might get passed to the database.

**Schema-based validation** checks the request body, query parameters, and route params against predefined schemas. Requests that don't match are rejected with a 400 response before any processing happens.

**Header hardening** adds HTTP security headers to every response, which protects clients from a range of browser-level attacks.

**Query sanitization** cleans incoming query parameters to block NoSQL injection attempts. Without this, an attacker could send something like `{ email: { "$ne": null } }` and bypass authentication checks entirely.

Rate limiting is also applied globally to prevent abuse and DDoS-style flooding.

```
  Incoming Request
        │
        ▼
  ┌─────────────────────────┐
  │   Security Middleware   │
  │   • Rate Limiting       │
  │   • Header Hardening    │
  │   • CORS Policy         │
  │   • Payload Size Limit  │
  └────────────┬────────────┘
               │
               ▼
  ┌─────────────────────────┐
  │  Validation Middleware  │
  │   • Body Schema         │
  │   • Query Params        │
  │   • Route Params        │
  │   • Input Sanitization  │
  └────────────┬────────────┘
               │
               ▼
           Controller
```

---

## Data Layer

### Schema Design

The models define the shape of data stored in MongoDB. They also encode data lifecycle rules — for example, session documents use TTL indexes so MongoDB automatically removes expired records without any manual cleanup job.

### Repository Pattern

All database access goes through the repository layer. Services never write raw MongoDB queries — they call repository methods. This means if you ever need to swap out MongoDB for a different database, you only need to rewrite the repositories. Everything above them stays the same.

### Indexing Strategy

Two types of indexes are used depending on the query pattern:

**Compound indexes** cover queries that filter on multiple fields together, such as fetching orders by status sorted by creation date. Without a compound index, MongoDB would scan the entire collection.

**Sparse indexes** are applied to optional fields. A sparse index only includes documents that actually contain the indexed field, which keeps the index small and efficient.

### Pagination

For large datasets, cursor-based pagination is preferred over offset pagination. Offset pagination using `skip()` gets slower as the page number grows because MongoDB still has to scan and discard all the earlier records. Cursor pagination uses the last document's ID as a bookmark, so it stays fast regardless of dataset size.

---

## Query Pipeline

Rather than writing a separate endpoint for every possible filter combination, the product API uses a dynamic query pipeline. A single endpoint accepts multiple optional parameters and constructs the database query at runtime based on what was provided.

```
  Incoming Request
        │
        ▼
  Parse Query Parameters
        │
        ▼
  Build Dynamic Filters
  (search, minPrice, maxPrice, tags)
        │
        ▼
  Apply Sorting
        │
        ▼
  Apply Cursor Pagination
        │
        ▼
  Execute Query
        │
        ▼
  Return Standardized Response
```

This makes the API much more flexible for clients and reduces the amount of route code that needs to be maintained.

---

## Async Job Processing

Some operations should not run inside the HTTP request-response cycle. Sending emails, generating reports, processing file uploads — these are slow and would block the API from responding quickly. For these, the system uses a background job queue backed by Redis.

```
  Client Request
        │
        ▼
    API Server
        │
        ▼
  Job Added to Queue
        │
        ▼
    Redis Queue
        │
        ▼
  Worker Process (separate)
        │
        ▼
  Job Execution
        │
        ▼
  Logs / Result
```

Workers run as completely separate processes from the API server. This means heavy background work doesn't compete with incoming requests for CPU time.

If a job fails, it isn't immediately dropped. The system applies a retry strategy with exponential backoff — it waits progressively longer between retries to avoid hammering a temporarily unavailable service.

---

## Observability

### Structured Logging

Logs are written using Winston in a structured format. Every log entry includes a timestamp, log level, service name, and message. This makes it possible to filter and search logs efficiently in production.

Log levels used: `info`, `warn`, `error`, `debug`

Logs are written to the `logs/` directory and also to stdout for container environments.

### Request Tracing

Every incoming request is assigned a unique `X-Request-ID`. This ID is attached to the request context and included in every log line generated during that request's lifecycle. When debugging an issue, you can search logs by request ID and reconstruct exactly what happened during that request across every layer of the application.

```
  Incoming Request
        │
        ▼
  Generate X-Request-ID
        │
        ▼
  Attach to Request Context
        │
        ▼
  Propagate Through All Layers
        │
        ▼
  Include in Every Log Entry
```

---

## Production Deployment

### Process Manager (PM2)

In production, the application runs under PM2. PM2 handles automatic restarts on crash, process monitoring, cluster mode for utilizing multiple CPU cores, and centralized log management. The configuration lives in `prod/ecosystem.config.js`.

### Environment Configuration

The `.env.example` file in the `prod/` folder documents every environment variable the application needs, with placeholder values. This makes it easy to onboard a new deployment environment without hunting through the codebase to figure out what variables are required.

### Graceful Shutdown

When the server receives a `SIGINT` or `SIGTERM` signal (for example, during a deployment rollout), it doesn't die immediately. It stops accepting new requests, waits for in-flight requests to complete, closes the database connection cleanly, and then exits. This prevents dropped requests and data corruption during restarts.

---

