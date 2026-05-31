---
description: Pinot query API reference.
---

# Broker Query API

Pinot exposes broker endpoints for single-stage execution, multi-stage execution, parse-only SQL syntax validation, and query fingerprint generation. Cursor-based pagination is available through query parameters on the SQL endpoint, and the response-store lifecycle is managed through broker endpoints on the same broker that executed the query.

For `POST /query/sql` and `POST /query`, malformed JSON request bodies and payloads that omit required fields return HTTP `400 Bad Request`. The helper endpoints on this page have endpoint-specific status handling, which is documented with each endpoint.

## Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/query/sql` | Submit SQL to the broker query endpoint |
| `POST` | `/query` | Submit SQL through the multi-stage endpoint |
| `POST` | `/query/sql/validateSyntax` | Parse SQL and report whether Pinot accepts the syntax |
| `POST` | `/query/sql/queryFingerprint` | Generate a normalized fingerprint and stable hash for a DQL query |
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

Both `POST /query/sql` and `POST /query` require a JSON request body with a top-level `sql` field. If the request body is malformed JSON or the `sql` field is missing, the broker returns HTTP `400 Bad Request`.

## SQL Syntax Validation

Use `POST /query/sql/validateSyntax` when you only need Pinot's Calcite-based parser to accept or reject the SQL text. The broker parses the statement but does not execute it, fetch table metadata, or run semantic validation.

This endpoint accepts both single-stage and multi-stage SQL, including statements that parse as `DQL`, `DML`, `DDL`, or `DCL`.

```bash
curl -H "Content-Type: application/json" -X POST \
  -d '{"sql":"SELECT * FROM myTable WHERE id > 10"}' \
  http://localhost:8099/query/sql/validateSyntax
```

Valid syntax returns HTTP `200 OK` with `valid=true` and the parsed SQL type:

```json
{
  "valid": true,
  "sqlType": "DQL"
}
```

Invalid syntax also returns HTTP `200 OK`, but with `valid=false` and parser error text:

```json
{
  "valid": false,
  "errorMessage": "Encountered \"FROM\" at line 1, column 8."
}
```

If the JSON payload omits the `sql` field, Pinot returns HTTP `400 Bad Request`:

```json
{
  "error": "Payload is missing the query string field 'sql'"
}
```

Malformed JSON and other unexpected server failures return HTTP `500 Internal Server Error`.

Compared with the related helper endpoints:

- Unlike `POST /query/sql/queryFingerprint`, this endpoint does not generate a fingerprint or query hash, and it is not limited to DQL.
- Unlike controller [`POST /validateMultiStageQuery`](controller-api.md), this endpoint is broker-local and parse-only. It does not compile the query against table metadata, validate semantics, or restrict validation to multi-stage queries.

## Query Fingerprints

Use `POST /query/sql/queryFingerprint` to generate a normalized fingerprint for a DQL query without executing it. Pinot returns a small JSON object with:

- `queryHash`: a stable hash of the normalized fingerprint
- `fingerprint`: the normalized SQL shape

The request body must include `sql`:

```bash
curl -H "Content-Type: application/json" -X POST \
  -d '{"sql":"SELECT * FROM myTable WHERE id IN (1, 2, 3)"}' \
  http://localhost:8099/query/sql/queryFingerprint
```

Pinot normalizes literals into placeholders, so the returned fingerprint for the example above is:

```text
SELECT * FROM `myTable` WHERE `id` IN (?)
```

The same endpoint also accepts multi-stage queries. For example, a query with `SET useMultistageEngine=true;` still returns a normalized fingerprint instead of executing the statement.

This endpoint is DQL-only. Malformed JSON, a missing `sql` field, invalid SQL, or a non-DQL statement all return HTTP `400 Bad Request`. Unlike the broker config `pinot.broker.enable.query.fingerprinting`, this helper endpoint can generate fingerprints on demand without enabling automatic fingerprinting for normal query execution.

## Cursor Pagination

Cursor-backed queries return the first page together with metadata that the client must reuse for later fetches. The most important fields are `requestId`, `brokerHost`, `brokerPort`, `offset`, `numRows`, `numRowsResultSet`, and `expirationTimeMs`.

```bash
curl --request POST http://localhost:8099/query/sql?getCursor=true&numRows=1 \
  --data '{"sql":"SELECT * FROM nation limit 100"}' | jq
```

If `numRows` is omitted or set to `0`, Pinot uses `pinot.broker.cursor.fetch.rows` (default `10000`). Fetch the next page with:

```bash
curl -X GET http://localhost:8099/responseStore/236490978000000006/results?offset=1&numRows=1 | jq
```

Read cursor metadata without returning the row slice:

```bash
curl -X GET http://localhost:8099/responseStore/236490978000000006 | jq
```

## Operational Notes

- Cursors are broker-affine; follow-up requests must go back to the same broker.
- Cursor results expire according to `pinot.broker.cursor.response.store.expiration` and are eventually cleaned up by the controller.
- `GET /responseStore` and `DELETE /responseStore/{requestId}` are operator-oriented response-store endpoints, not the normal client pagination flow.

## What this page covered

- The broker query endpoints and their intended use.
- Parse-only syntax validation versus fingerprint generation and controller-side validation.
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
- [Query using Cursors](../../build-with-pinot/querying-and-sql/query-execution-controls/query-using-cursors.md)
