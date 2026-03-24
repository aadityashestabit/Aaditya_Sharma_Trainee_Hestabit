# Reverse Proxy Setup — Day 3 (NGINX + Load Balancing)

## Overview

Using NGINX as a reverse proxy inside Docker to route incoming requests to backend services.

Instead of exposing backend services directly, all traffic first goes through NGINX. This mimics how real production systems handle routing, security, and scalability.

We also simulate load balancing by running multiple instances of the backend.

---

## Architecture Components

### 1. NGINX (Reverse Proxy)
- Entry point for all incoming requests
- Routes traffic to appropriate services
- Handles load balancing across backend replicas

### 2. Backend Services (Node.js)
- Multiple instances of the same backend service
- Handle API requests
- Connected behind NGINX

### 3. Client (React)
- Sends requests to NGINX instead of directly calling backend

---

## High-Level Architecture Diagram
```
             ┌───────────────┐
             │   Browser     │
             │ (User Client) │
             └──────┬────────┘
                    │ HTTP Request
                    ▼
           ┌────────────────────┐
           │       NGINX        │
           │   Reverse Proxy    │
           └──────┬─────┬──────-┘
                  │     │
      ┌───────────┘     └───────────┐
      ▼                             ▼
    ┌────────────────┐ ┌────────────────┐
    │ Backend #1     │ │ Backend #2     │
    │ (Node.js)      │ │ (Node.js)      │
    └────────┬───────┘ └────────┬───────┘
        │                             │
        └──────────────┬──────────────┘
                       ▼
               ┌────────────────┐
               │ MongoDB        │
               └────────────────┘
```


---

## Why Reverse Proxy?

Without NGINX:
- Client directly calls backend
- Hard to scale
- No centralized routing

With NGINX:
- Single entry point
- Easy to add more backend instances
- Enables load balancing
- Improves security and abstraction

---
