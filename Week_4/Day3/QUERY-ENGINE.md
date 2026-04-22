# QUERY-ENGINE.md

## Day 3 — Query Pipelines & Cursor-Based Pagination

---

## What Is the Query Engine

The query engine is the part of the service layer responsible for translating raw HTTP query parameters into a safe, performant MongoDB query. Rather than building a separate database call for every possible combination of filters and sort orders, a single engine receives whatever the client sends, assembles the query dynamically, and executes it. This keeps the controller thin and makes the filtering logic easy to extend without touching route or controller code.

The engine handles four concerns in sequence: filtering, sorting, cursor resolution, and finally result fetching with metadata assembly.

---

## Why Cursor-Based Pagination Over Skip/Limit

Before getting into the implementation, it is worth understanding why cursor pagination exists in the first place.

With offset pagination you tell the database "skip the first N documents and give me the next 10." This sounds simple and works fine on small collections. The problem is that MongoDB still has to scan and discard all the documents before your offset before it can return your page. On a collection with 500,000 orders, fetching page 1000 means MongoDB internally traverses 10,000 documents just to throw them away. The query gets slower as the page number grows, and there is nothing an index can do to fully rescue it.

Cursor pagination works differently. Instead of saying "skip to page N," you say "give me documents that come after this specific document." The cursor is typically the `_id` of the last document the client received. Because MongoDB's `_id` is a monotonically increasing ObjectId, and because `_id` is always indexed, the database can jump directly to the right position in the index without scanning anything before it. Query time stays consistent whether you are on page 1 or page 50,000.

There is one trade-off: you cannot jump to an arbitrary page number. Cursor pagination only supports "next page" and "previous page" navigation. For most product APIs, admin dashboards, and feed-style interfaces this is perfectly acceptable and often preferable from a UX standpoint anyway.

---

## The Cursor Format

The system uses MongoDB's `_id` field as the cursor value. `_id` is a BSON ObjectId which encodes a timestamp in its first four bytes, making it naturally sortable by creation time without needing a separate `createdAt` sort field (though sorting by `createdAt` with `_id` as a tiebreaker is also valid and used here).

The cursor passed between client and server is the raw ObjectId string of the last document on the current page. The client stores this value and sends it back on the next request as a query parameter.

```
GET /api/v1/products?limit=10
GET /api/v1/products?limit=10&cursor=65e0a1b2c3d4e5f6a7b8c9d0&direction=next
GET /api/v1/products?limit=10&cursor=65e0a1b2c3d4e5f6a7b8c9d0&direction=prev
```

The `direction` parameter tells the engine whether the client is moving forward or backward through the dataset.

---

## Building the Filter Object

Before pagination is applied, the engine assembles a filter object from the incoming query parameters. This is a plain JavaScript object that will be passed directly to `collection.find()`.

The supported filter parameters are:

- `search` — performs a case-insensitive regex match across `title` and `description`
- `category` — exact match on the category field
- `brand` — exact match on the brand field
- `minPrice` and `maxPrice` — assembled into a single `$gte`/`$lte` range on the `price` field
- `isActive` — boolean filter to show only active or inactive products
- `tags` — accepts a comma-separated list and uses `$in` to match any document containing at least one of the provided tags

All soft-deleted documents are always excluded by appending `isDeleted: false` to every filter object before the query runs. This is non-negotiable and hardcoded in the engine rather than relying on callers to remember to add it.

---

## Building the Sort Object

Sorting is parsed from a `sort` query parameter in the format `field:direction`.

```
GET /api/v1/products?sort=price:asc
GET /api/v1/products?sort=createdAt:desc
```

The engine parses this string and converts it into the MongoDB sort object. If no sort is provided, it defaults to `{ createdAt: -1 }` which returns the newest documents first. A secondary sort on `_id` is always appended as a tiebreaker to guarantee stable ordering when two documents have identical values on the primary sort field. Without this tiebreaker, cursor pagination can produce duplicates or skip documents when pages straddle documents with equal sort values.

---


This is necessary because MongoDB returns the documents in the order dictated by the sort, but for a previous page request we fetched them "backwards" through the index. Reversing restores the natural display order.

---

## Assembling the Response

After the query runs, the engine assembles a response object that gives the client everything it needs to navigate pages without any server-side session state.

The `nextCursor` is the `_id` of the last document in the current result set. The client sends this back when requesting the next page.

The `prevCursor` is the `_id` of the first document in the current result set. The client sends this back when requesting the previous page.

The service layer calls this function and passes the result directly up to the controller, which serializes it as the HTTP response.

---

## Example Walkthrough

Say a client fetches the first page of products filtered by category "electronics", sorted by price descending, with a limit of 5.

```
GET /api/v1/products?category=electronics&sort=price:desc&limit=5
```

The engine builds the filter `{ isDeleted: false, category: "electronics" }` and sort `{ price: -1, _id: -1 }`. No cursor is present so no cursor condition is injected. Six documents are fetched. Five are returned. The last document's `_id` is included in the response as `nextCursor`.

The client now wants the next page:

```
GET /api/v1/products?category=electronics&sort=price:desc&limit=5&cursor=65e0a1b2c3d4e5f6a7b8c9d0&direction=next
```

The engine builds the same filter, then appends `_id: { $lt: ObjectId("65e0a1b2...") }` because the sort is descending. MongoDB jumps directly to that `_id` in the index and scans forward. Six documents are fetched. Five are returned. The response contains both a `nextCursor` (the last document's `_id`) and a `prevCursor` (the first document's `_id`).

The client now wants to go back:

```
GET /api/v1/products?category=electronics&sort=price:desc&limit=5&cursor=65e1a2b3c4d5e6f7a8b9c0d1&direction=prev
```

The engine appends `_id: { $gt: ObjectId("65e1a2...") }`, reverses the sort to `{ price: 1, _id: 1 }`, fetches six documents, reverses the results array, and returns the previous five in the correct display order.

---

## Important Edge Cases

**First page with no cursor** — the cursor condition is skipped entirely and all documents matching the filter are eligible. The `prevCursor` in the response will be null since there is no page before the first page.

**Empty result set** — if no documents match the filter, both cursors are null and both `hasNextPage` and `hasPrevPage` are false.

**Cursor pointing to a deleted document** — because soft-deleted documents are always excluded via `isDeleted: false`, a cursor pointing to a document that was later soft-deleted will still work correctly. The `_id` comparison is a positional boundary, not a reference to the document itself, so the deleted document's absence from results does not cause a gap or error.

**Limit clamping** — the engine enforces a maximum limit of 100 regardless of what the client requests. This prevents a client from accidentally or intentionally dumping the entire collection in a single request.

---

## Summary

Cursor pagination is faster than offset pagination because it trades random-access page jumping for sequential navigation, which maps directly onto how database indexes work. The engine described here handles both forward and backward navigation using a single cursor value, keeps all pagination state on the client, and integrates cleanly with the dynamic filter and sort system so that every combination of filters continues to paginate correctly without any special casing.