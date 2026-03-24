# Service Architecture — Day 2 (Docker Compose Multi-Container Setup)

## Overview

In this setup, we move from running a single container to orchestrating a full-stack application using Docker Compose.

The system consists of three main services:

- Client (React frontend)
- Server (Node.js backend)
- Database (MongoDB)

All services run in isolated containers but communicate with each other through Docker's internal network.

---

## Architecture Components

### 1. Client (React App)
- Runs on a development server
- Responsible for UI rendering
- Sends API requests to the backend server

### 2. Server (Node.js API)
- Handles business logic
- Exposes REST APIs (e.g., `/api`)
- Connects to MongoDB using Docker network hostname

### 3. Database (MongoDB)
- Stores application data
- Uses Docker volume for persistence
- Accessible only within Docker network

---

## High-Level Architecture Diagram
```
      ┌───────────────┐
      │   Browser     │
      │ (User Client) │
      └──────┬────────┘
             │ HTTP Requests
             ▼
    ┌────────────────────┐
    │  React Frontend    │
    │  (Client Service)  │
    └────────┬───────────┘
             │ API Calls (/api)
             ▼
    ┌────────────────────┐
    │  Node.js Backend   │
    │  (Server Service)  │
    └────────┬───────────┘
             │ DB Queries
             ▼
    ┌────────────────────┐
    │     MongoDB        │
    │   (DB Service)     │
    └────────────────────┘
```


---

## Docker Networking

Docker Compose automatically creates a shared network for all services.

- Each service can be accessed using its service name as hostname
- Example:
  - Backend connects to MongoDB using `mongodb://mongo:27017`
  - `mongo` is the service name defined in `docker-compose.yml`

---

## Request Flow (Step-by-Step)

### User Request Flow
1. User opens the application in browser
2. React app loads from client container
3. User performs an action
4. React sends API request to backend
5. Backend processes request
6. Backend queries MongoDB
7. MongoDB returns data
8. Backend sends response to client
9. Client updates UI


- Client talks to server via HTTP
- Server talks to MongoDB via database connection protocol
- MongoDB is not exposed publicly

---

## Volumes and Persistence

MongoDB uses a Docker volume to persist data.

### Why this is important:
- Data is not lost when container stops
- Enables production-like behavior
