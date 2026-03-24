---
description: Pinot query API reference.
---

# Broker Query API

Pinot exposes two broker query endpoints: `/query/sql` for the single-stage path and `/query` for multi-stage execution. Cursor-based pagination is available through query parameters on the SQL endpoint, and the response-store lifecycle is managed through broker endpoints on the same broker that executed the query.

## Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/query/sql` | Submit SQL to the broker query endpoint |
| `POST` | `/query` | Submit SQL through the multi-stage endpoint |
| `POST` | `/query/sql?getCursor=true` | Submit a query and return a cursor-backed first page |
| `GET` | `/responseStore/{requestId}/results` | Fetch additional cursor pages |
| `GET` | `/responseStore/{requestId}` | Fetch cursor metadata |
| `GET` | `/responseStore` | List active cursor stores |
| `DELETE` | `/responseStore/{requestId}` | Delete a cursor response store |

## Query Submission

```bash
curl -H "Content-Type: application/json" -X POST \
  -d '{"sql":"select foo, count(*) from myTable group by foo limit 100"}' \
  http://localhost:8099/query/sql
```

Use `/query` when the statement requires multi-stage features such as joins or window functions:

```bash
curl -H "Content-Type: application/json" -X POST \
  -d '{"sql":"select count(*) from a JOIN b ON a.x = b.x"}' \
  http://localhost:8099/query
```

## Cursor Pagination

The cursor flow returns a `requestId`, `brokerHost`, and `brokerPort` that the client must reuse for subsequent fetches.

```bash
curl --request POST http://localhost:8099/query/sql?getCursor=true&numRows=1 \
  --data '{"sql":"SELECT * FROM nation limit 100"}' | jq
```

The page size is controlled by the request parameter and the broker cursor defaults. Fetch the next page with:

```bash
curl -X GET http://localhost:8099/responseStore/236490978000000006/results?offset=1&numRows=1 | jq
```

## Operational Notes

- Cursors are broker-affine; follow-up requests must go back to the same broker.
- The response store is eventually cleaned up by the controller.
- `GET /responseStore` is useful for operational inspection, not for client pagination.

## What this page covered

- The broker query endpoints and their intended use.
- Cursor-based pagination and response-store lifecycle basics.
- The main operational constraint: follow-up requests must hit the same broker.

## Next step

If you need SQL semantics rather than transport semantics, jump to the SQL syntax page; if you need endpoint details beyond query submission, move to the controller or gRPC reference.

## Related pages

- [API Reference](README.md)
- [Query Response Format](query-response-format.md)
- [Controller Admin API](controller-admin-api.md)
- [Broker gRPC API](broker-grpc-api.md)
- [Querying Pinot](../../build-with-pinot/querying-and-sql/querying-pinot.md)
- [Query using Cursors](../../users/user-guide-query/query-using-cursors.md)
