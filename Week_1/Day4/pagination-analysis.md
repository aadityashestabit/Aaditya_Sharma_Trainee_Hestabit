---
## Pagination Analysis

### Request
GET /users/octocat/repos?page=1&per_page=5

### Observed Headers
- HTTP Status: 200 OK
- `Link` header is present
- Rate limit remaining: 50

### Link Header Value
<https://api.github.com/user/583231/repos?page=2&per_page=5>; rel="next",
<https://api.github.com/user/583231/repos?page=2&per_page=5>; rel="last"

### Obeserve
- The `next` and `last` links both points to page 2
- This indicates there are **only two pages** of results for this query
- GitHub uses an internal URL (`/user/583231`) in pagination links

### Navigation Strategy
- Start with page=1
- Follow `rel="next"` until the page referenced by `rel="last"`
- Stop when the current page equals the `last` page
---