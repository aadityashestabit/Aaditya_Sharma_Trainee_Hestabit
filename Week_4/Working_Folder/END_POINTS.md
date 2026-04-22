# API Endpoints

This section documents the available API endpoints for **User** and **Product** modules.

Base URL

```
/api
```

---

# User API Endpoints

| Method | Endpoint | Description | Middleware |
|------|------|------|------|
| POST | `/api/users/create` | Create a new user account | Validation |
| POST | `/api/users/login` | Authenticate user and generate token | None |
| GET | `/api/users/` | Get all users | Authentication |
| GET | `/api/users/:id` | Get a single user by ID | Authentication |
| PATCH | `/api/users/:id` | Update user information | Validation + Authentication |
| DELETE | `/api/users/:id` | Delete user | Authentication |

---

# Product API Endpoints

| Method | Endpoint | Description | Middleware |
|------|------|------|------|
| POST | `/api/products/` | Create a new product | Authentication + Validation |
| GET | `/api/products/` | Get all products | Authentication |
| GET | `/api/products/:id` | Get product by ID | Authentication |
| PATCH | `/api/products/:id` | Update product | Authentication + Validation |
| DELETE | `/api/products/:id` | Delete product | Authentication |

---

# Middleware Overview

| Middleware | Purpose |
|------|------|
| authenticate | Verifies JWT token and protects routes |
| validate(schema) | Validates request payload using schema |
| error middleware | Handles global API errors |

---

# API Response Format

Success response

```
{
  "success": true,
  "data": {},
  "message": "Request successful"
}
```

Error response

```
{
  "success": false,
  "message": "Error description",
  "code": "ERROR_CODE",
  "timestamp": "ISO timestamp",
  "path": "/api/resource"
}
```



```

GET /api/products?cursor=xyz456&direction=prev
```