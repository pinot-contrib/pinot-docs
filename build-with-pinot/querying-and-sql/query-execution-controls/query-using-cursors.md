---
description: Cursor pagination for large Pinot result sets.
---

# Querying Pinot Using Cursors

Cursor pagination lets Pinot return a query result in pages. The broker keeps the full result in its response store. The client then fetches one page at a time.

## When to use it

Use cursor pagination when:

- the result set is large
- the client shows the result one page at a time
- the client cannot keep the full result in memory

## Submit a cursor-backed query

Send the query to `POST /query/sql` with `getCursor=true`. For the multi-stage engine, use `POST /query`.

```sh
curl --request POST 'http://localhost:8099/query/sql?getCursor=true&numRows=1000' \
  --header 'Content-Type: application/json' \
  --data '{"sql":"SELECT * FROM nation LIMIT 100000"}'
```

`numRows` sets the page size. If `numRows` is omitted or set to `0`, Pinot uses the broker config `pinot.broker.cursor.fetch.rows` (default `10000`).

Cursors support only DQL (`SELECT`) statements. The `GET` query endpoints do not support cursors. If the query fails, Pinot returns the normal error response and does not store a result.

The first response contains the first page in `resultTable`, together with cursor metadata:

| Field | Meaning |
| --- | --- |
| `requestId` | Cursor identifier used in later fetches |
| `numRowsResultSet` | Total rows available across the full result set |
| `offset` | Zero-based offset of the current page |
| `numRows` | Number of rows returned in the current page |
| `brokerHost` / `brokerPort` | Broker that owns the cursor state |
| `submissionTimeMs` | When Pinot created the response-store entry |
| `expirationTimeMs` | When the cursor expires |

## Fetch the next page

```sh
curl -X GET 'http://localhost:8099/responseStore/236490978000000006/results?offset=1000&numRows=1000'
```

- `offset` is required and zero-based. It must be less than `numRowsResultSet`.
- `numRows` is optional. If you omit it, Pinot uses `pinot.broker.cursor.fetch.rows`.
- Send each fetch to the broker that created the cursor (`brokerHost` and `brokerPort`).

### Example: read all pages

```python
import requests

BROKER = "http://localhost:8099"  # Must be the broker that runs the query.
PAGE_SIZE = 1000

first = requests.post(
    f"{BROKER}/query/sql",
    params={"getCursor": "true", "numRows": PAGE_SIZE},
    json={"sql": "SELECT * FROM my_table LIMIT 1000000"},
).json()

request_id = first["requestId"]
total = first["numRowsResultSet"]
rows = first["resultTable"]["rows"]
# Process rows.

offset = first["offset"] + first["numRows"]
while offset < total:
    page = requests.get(
        f"{BROKER}/responseStore/{request_id}/results",
        params={"offset": offset, "numRows": PAGE_SIZE},
    ).json()
    rows = page["resultTable"]["rows"]
    # Process rows.
    offset += page["numRows"]

# Optional: delete the stored result now. Otherwise the broker deletes it after it expires.
requests.delete(f"{BROKER}/responseStore/{request_id}")
```

## Inspect or delete cursor state

These endpoints are for operators. A normal client pagination flow does not need them.

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/responseStore/{requestId}` | Get cursor metadata without the rows |
| `GET` | `/responseStore` | List metadata for all entries in the broker response store |
| `DELETE` | `/responseStore/{requestId}` | Delete one stored result |
| `DELETE` | `/responseStore?expiredBefore={epochMs}` | Delete all expired results |

The batch delete deletes each entry whose `expirationTimeMs` is at or before `expiredBefore`. If you omit `expiredBefore`, Pinot uses the current time.

```sh
# Delete all results that are expired now.
curl -X DELETE 'http://localhost:8099/responseStore'

# Delete all results that expired at or before a given epoch-millisecond time.
curl -X DELETE 'http://localhost:8099/responseStore?expiredBefore=1776816000000'
```

The response is plain text:

```
Deleted 42 expired response(s).
```

## Broker cursor cleanup configuration

Each stored result expires at `submissionTimeMs` plus `pinot.broker.cursor.response.store.expiration`. Each broker runs a background task that deletes the expired results from its response store.

Set these properties in the broker config:

| Config | Default | Description |
| --- | --- | --- |
| `pinot.broker.cursor.response.store.expiration` | `1h` | Time after submission when a stored result expires. |
| `pinot.broker.cursor.response.store.cleaner.frequencyPeriod` | `1h` | Interval between two cleanup runs. Must be more than `0`. |
| `pinot.broker.cursor.response.store.cleaner.initialDelay` | not set | Delay before the first cleanup run. If not set, the first run starts after one `frequencyPeriod` plus a random delay of up to 25% of `frequencyPeriod`. The random delay stops brokers that share storage from running cleanup at the same time. |

All three values are period strings, for example `30m`, `1h`, or `1d`. The broker reads them only at startup. Restart the broker to apply a change.

```properties
pinot.broker.cursor.response.store.expiration=1h
pinot.broker.cursor.response.store.cleaner.frequencyPeriod=15m
pinot.broker.cursor.response.store.cleaner.initialDelay=5m
```

For the response store type and file locations, see the [broker configuration reference](../../../reference/configuration-reference/broker.md).

## Upgrade note: cleanup moved from controller to broker

Starting in Pinot 1.6.0 ([apache/pinot#18203](https://github.com/apache/pinot/pull/18203)), each broker deletes its own expired cursor results. The controller no longer runs the `ResponseStoreCleaner` periodic task.

- The controller configs `controller.cluster.response.store.cleaner.frequencyPeriod` and `controller.cluster.response.store.cleaner.initialDelay` have no effect. Move custom values to the `pinot.broker.cursor.response.store.cleaner.*` broker configs above.
- During a rolling upgrade, upgraded controllers and old brokers do not delete expired results. These results stay in the response store until you upgrade the brokers. Upgrade the brokers soon after the controllers.
- Old brokers do not have the batch `DELETE /responseStore` endpoint. To delete results on an old broker, use `DELETE /responseStore/{requestId}`.

## What this page covered

This page covered how to submit a cursor-backed query, fetch more pages, inspect or delete cursor state, and configure broker-side cleanup.

## Next step

If you need to trace a query or cancel it later, read [Correlation IDs](query-correlation-id.md) and [Query cancellation](query-cancellation.md).

## Related pages

- [Query options](query-options.md)
- [Query cancellation](query-cancellation.md)
- [Querying Pinot](../querying-pinot.md)
- [Query API](../../../reference/api-reference/query-api.md)
- [Pinot broker configuration](../../../reference/configuration-reference/broker.md)
