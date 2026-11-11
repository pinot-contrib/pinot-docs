---
description: Limit the size of the response that each server sends to the broker in single-stage queries.
---

# Server Response Size Limits

A single-stage query can make each server send a large response to the broker. For example, a `GROUP BY` with a high `LIMIT` and sketch aggregations can return tens of megabytes per server. The broker must hold all of these responses in memory at the same time.

You can set a limit on the size of the response of each server. If a response is larger than the limit, the server sends an error instead of the rows.

## Scope

The limit applies only to these queries:

- Single-stage queries. The multi-stage engine does not use this limit.
- Responses that the server sends to the broker through the Netty query channel. The gRPC query server does not use this limit.

By default, there is no limit.

## Settings

There are two settings. Each one has a query option, a table setting, and a broker setting.

| Setting | Meaning |
|---|---|
| `maxServerResponseSizeBytes` | The maximum size of the serialized response of one server, in bytes. |
| `maxQueryResponseSizeBytes` | The maximum size of the serialized responses of all servers together, in bytes. The broker divides this value by the number of servers that the query uses, and uses the result as the limit for each server. |

| Level | Server limit | Query limit |
|---|---|---|
| Query option | `maxServerResponseSizeBytes` | `maxQueryResponseSizeBytes` |
| Table config, in `query` | `maxServerResponseSizeBytes` | `maxQueryResponseSizeBytes` |
| Broker config | `pinot.broker.max.server.response.size.bytes` | `pinot.broker.max.query.response.size.bytes` |

The query options and the table settings accept a number of bytes. The value must be more than 0. The broker settings also accept a size with a unit, for example `100M` or `1.5G`. The units are powers of 1024.

## Order of priority

For each query, the broker uses the first value that it finds in this list:

1. The query option `maxServerResponseSizeBytes`.
2. The query option `maxQueryResponseSizeBytes`, divided by the number of servers.
3. The table setting `maxServerResponseSizeBytes`.
4. The table setting `maxQueryResponseSizeBytes`, divided by the number of servers.
5. The broker setting `pinot.broker.max.server.response.size.bytes`.
6. The broker setting `pinot.broker.max.query.response.size.bytes`, divided by the number of servers.

If the broker finds no value, the servers do not limit the response size.

For a hybrid table, the broker calculates one limit for the offline table and one limit for the realtime table. Each calculation uses the table config of that table. The number of servers is the total of the offline and realtime servers.

## Examples

Set a limit of 50 MB for each server in one query:

```sql
SELECT customerId, DISTINCTCOUNTHLLPLUS(sessionId)
FROM events
GROUP BY customerId
LIMIT 100000
OPTION(maxServerResponseSizeBytes=52428800)
```

Set a limit of 200 MB for all servers together, for all the queries on a table:

```json
{
  "tableName": "events",
  "tableType": "OFFLINE",
  "query": {
    "maxQueryResponseSizeBytes": 209715200
  }
}
```

Set a default limit of 100 MB for each server, for all the queries of a broker:

```properties
pinot.broker.max.server.response.size.bytes=100M
```

## What happens when a response is too large

The server compares the size of the response with the limit at two points:

1. While it builds the response. After each row, the server compares the bytes written so far with the limit. If they are more than the limit, the server stops and discards the rows.
2. After it serializes the full response. This comparison also counts the header, the data schema and the metadata of the response.

At either point, the server does these steps if the response is larger than the limit:

1. It sends an error with the code `QueryCancellationError` (503) to the broker. The message starts with `Serialized query response size` and contains the limit.
2. It increments the `largeQueryResponseSizeExceptions` meter for the table.

The broker returns this error in the `exceptions` field of the query response. The results of the other servers stay in the response, so the result is partial.

The server records the size of every response that it sends in the `queryResponseSize` meter for the table. Use this meter to find a good limit before you set it.

## Memory of the server

Because the server stops while it builds the response, it never holds much more than the limit for one response. Without a configured limit, the server stops at 2 GB, which is the maximum size of the wire format.

The response is also visible to the query resource accountant while the server builds it. The server samples the memory of the query for each 1 MB that it writes. Thus the accountant can stop a query with a large response even if the response has few rows.
