---
description: Lightweight overview of Pinot broker and controller APIs plus gRPC entrypoints.
---

# REST / gRPC APIs

Use Pinot APIs when you need programmatic access rather than a direct client library or BI connector. The main surfaces are broker query APIs for SQL, broker gRPC for higher-throughput query clients, and controller APIs for cluster and table administration.

## What belongs here

| Surface | Best for | Notes |
| --- | --- | --- |
| Broker REST query APIs | SQL queries from applications or scripts | The broker exposes the query endpoints used by the query console and the standard SQL docs. |
| Broker gRPC API | Higher-throughput query clients | The gRPC surface supports binary transport and client-specific encoding or compression options. |
| Controller admin APIs | Cluster, schema, table, segment, quota, and task operations | The controller is the management surface and is what the Admin UI exposes through Swagger. |

## How to choose

Use broker REST if you want the most familiar query flow and do not need gRPC transport. Use broker gRPC when you care about client-side efficiency or want a gRPC transport layer. Use controller APIs when you are changing metadata or managing the cluster rather than querying data.

The detailed endpoint inventory belongs in Reference > API reference. This page stays intentionally light and points you toward the right surface instead of duplicating every endpoint.

## Detailed docs

* [API reference](../../reference/api-reference/README.md)
* [Broker Query API](../../reference/api-reference/query-api.md)
* [Query Response Format](../../reference/api-reference/query-response-format.md)
* [Broker gRPC API](../../reference/api-reference/broker-grpc-api.md)
* [Controller API Examples](../../reference/api-reference/controller-api.md)
* [Controller Admin API](../../reference/api-reference/controller-admin-api.md)

## What this page covered

This page covered the three programmatic API surfaces most users reach for: broker REST queries, broker gRPC queries, and controller administration.

## Next step

Use the broker query docs for SQL access or the controller docs for metadata and cluster operations, then move to Reference for the full endpoint inventory.

## Related pages

* [Client libraries](client-libraries.md)
* [Querying Pinot](../querying-and-sql/querying-pinot.md)
* [Configuration reference](../../reference/configuration-reference/README.md)
* [API reference](../../reference/api-reference/README.md)
