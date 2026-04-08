---
description: Build applications with Pinot client libraries for Java, JDBC, Python, and Go.
---

# Client libraries

Use client libraries when your application code needs to query Pinot directly instead of going through a BI tool or a federated SQL engine. The client path is best when you want broker-aware routing, async queries, prepared statements, or direct access to Pinot result sets.

## What belongs here

| Client | Best for | Notes |
| --- | --- | --- |
| Java | JVM services and libraries | Native query client with blocking and async execution, prepared statements, request tracing, and tenant-aware broker selection. The same `org.apache.pinot:pinot-java-client:1.4.0` artifact also ships the controller-facing Java admin client. |
| JDBC | SQL-first applications and BI plumbing | Standard JDBC interface that is easy to embed in SQL tooling. The linked docs use `org.apache.pinot:pinot-jdbc-client:1.4.0`. |
| Python | Data apps, notebooks, and SQLAlchemy workflows | DB-API and SQLAlchemy support through `pinotdb`. The linked docs call out SQL API support in `pinotdb` 0.3.2+ and older PQL compatibility in 0.2.x. |
| Go | Services and batch tools written in Go | Native Go client with direct SQL execution and response inspection. |

## How to choose

Choose Java when you want the most direct Pinot-native API surface in a JVM application. Use the Java query client for broker-routed SQL execution, and use the Java admin client when JVM code needs the controller REST APIs for tables, schemas, segments, instances, tenants, or tasks. Choose JDBC when the consuming tool expects a database driver. Choose Python when you need a notebook-friendly or ORM-friendly connection. Choose Go when you want a thin client in a Go service or pipeline.

The Java and JDBC client docs both use `1.4.0` artifacts in their current installation examples. Keep those two examples aligned when you refresh the client docs so the dependency versions do not drift apart.

## Detailed docs

* [Java client](clients/java.md)
* [Java admin client](clients/java-admin-client.md)
* [JDBC client](clients/jdbc.md)
* [Python client](clients/python.md)
* [Go client](clients/golang.md)

## What this page covered

This page covered the four direct client options for application code that queries Pinot without a BI tool or federated engine.

## Next step

Open the detail page for the language you are using and follow the connection pattern, authentication, and timeout guidance there.

## Related pages

* [BI tools](bi-tools.md)
* [REST / gRPC APIs](rest-grpc-apis.md)
* [Querying Pinot](../querying-and-sql/querying-pinot.md)
