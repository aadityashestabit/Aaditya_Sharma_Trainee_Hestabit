# SSL Certificate Setup — Day 4 (HTTPS + mkcert + NGINX)

## Overview

In this setup, we enable HTTPS for our application using SSL/TLS certificates.

Instead of serving traffic over insecure HTTP, we configure NGINX to terminate HTTPS connections and securely forward requests to internal services.

We use `mkcert` to generate locally trusted self-signed certificates for development.

---

## Architecture Components

### 1. NGINX (SSL Termination Point)
- Handles HTTPS connections
- Decrypts incoming traffic
- Forwards requests to backend services over internal network

### 2. SSL Certificates
- Public certificate (`cert.pem`)
- Private key (`key.pem`)
- Mounted inside NGINX container

### 3. Backend Services
- Continue running on HTTP internally
- Not exposed directly to users

---

## High-Level Architecture Diagram
```
             ┌───────────────┐
             │   Browser     │
             │  (HTTPS User) │
             └──────┬────────┘
                    │ HTTPS (SSL/TLS)
                    ▼
           ┌────────────────────┐
           │       NGINX        │
           │  SSL Termination   │
           └──────┬─────────────┘
                  │ HTTP (Internal)
                  ▼
           ┌────────────────────┐
           │    Backend API     │
           │    (Node.js)       │
           └────────┬───────────┘
                    │
                    ▼
           ┌────────────────────┐
           │      MongoDB       │
           └────────────────────┘
```



---

## Why HTTPS?

HTTP problems:
- Data sent in plain text
- Vulnerable to interception (MITM attacks)

HTTPS benefits:
- Encrypted communication
- Data integrity
- Trust (browser lock icon)

---

## What is SSL/TLS?

SSL/TLS is a protocol that encrypts communication between client and server.

Key components:
- Certificate → proves server identity
- Private key → used for encryption/decryption

---

## mkcert for Local Development

`mkcert` allows us to generate locally trusted certificates without browser warnings.

### Steps:
1.mkcert -install \ 
2.mkcert localhost


This generates:
- `localhost.pem` (certificate)
- `localhost-key.pem` (private key)

---

## NGINX SSL Configuration

### 1. Listen on HTTPS
server {\
listen 443 ssl;\
}


### 2. Attach Certificates
ssl_certificate /etc/nginx/certs/cert.pem\
ssl_certificate_key /etc/nginx/certs/key.pem


### 3. Proxy to Backend
location /api {\
proxy_pass http://backend_service;\
}


---

## HTTP to HTTPS Redirect

Force all HTTP traffic to HTTPS:
server {\
listen 80;\
return 301 https://$host$request_uri;\
}