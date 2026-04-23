# Week 4 — Day 4: API Defense & Input Control

> **Backend Systems & Production Engineering**

---

## Overview

Day 4 focuses on securing Express/Node.js APIs against common backend threats. This includes setting up a defensive middleware stack, validating and sanitizing all incoming input, and implementing rate limiting and payload controls to harden the API surface.

---

## 1. Common Backend Threats

### NoSQL Injection
- Attackers craft malicious query objects to manipulate MongoDB operations.
- **Example:** Passing `{ "$gt": "" }` in a login field to bypass authentication.
- **Prevention:** Validate and sanitize all query parameters before DB operations.

### Cross-Site Scripting (XSS)
- Malicious scripts injected into responses and executed in a user's browser.
- **Prevention:** Sanitize input, escape output, and use Helmet to set secure headers.

### Parameter Pollution (HPP)
- Sending duplicate query parameters to confuse parsing logic.
- **Example:** `?sort=name&sort=password` overrides expected sort behavior.
- **Prevention:** Use `express-mongo-sanitize` and `hpp` middleware.

### Brute-Force Attacks
- Repeated automated requests to guess passwords or tokens.
- **Prevention:** Rate limiting with `express-rate-limit`.

---

## 2. Defensive Middleware Stack

### Install Required Packages

```bash
npm install helmet cors express-rate-limit express-mongo-sanitize hpp joi
```

| Middleware | Purpose |
|---|---|
| `helmet` | Sets secure HTTP headers (XSS, clickjacking, MIME sniffing) |
| `cors` | Restricts which origins can call the API |
| `express-rate-limit` | Limits requests per IP within a time window |
| `express-mongo-sanitize` | Strips MongoDB operators from request input |
| `hpp` | Prevents HTTP parameter pollution |
| `joi` / `zod` | Schema-based request validation |

---

## 3. Validation as Core Logic

### Schema-Level Validation
- Define expected shape, types, and constraints for every incoming request.
- Validation schemas should live in a dedicated `/validators` directory.

### Whitelisting Allowed Fields
- Only accept fields your application explicitly expects.
- Strip out any extra fields not defined in the schema.

### Rejecting Unknown Properties
- Use `.unknown(false)` in Joi or `.strict()` in Zod to block unexpected keys.
- Prevents attackers from injecting unexpected fields into the database.

### Sanitizing Query Parameters
- Strip MongoDB operators like `$gt`, `$where` from all query inputs.
- Use `express-mongo-sanitize` as middleware to automate this.

---


## 4. Directory Structure

```
project/
├── middlewares/
│   ├── securityMiddlewares.js   # Helmet, CORS, rate limit, sanitize, hpp
│   └── validate.js              # Joi/Zod validation helpers
├── validators/
│   ├── authValidator.js         # Login / register schemas
│   └── userValidator.js         # Profile update schemas
├── app.js                       # Middleware registration
└── .env                         # ALLOWED_ORIGIN and other secrets
```

> **Note:** Security middleware must be registered **before** route handlers in `app.js`.

---

