---
description: Use Flink and Spark to read from or write to Pinot in batch and streaming pipelines.
---

# Processing connectors

Use processing connectors when Pinot is part of a larger Flink or Spark job and the data movement should stay inside that processing framework. These connectors are for read or write integration, not for the simpler ingestion flows covered elsewhere in the docs.

## What belongs here

| Connector | Best for | Notes |
| --- | --- | --- |
| Flink connector | Streaming or batch jobs that write into Pinot | The current guide focuses on the `PinotSinkFunction`, offline and realtime table support, and upsert bootstrapping. |
| Spark-Pinot connector | Spark jobs that read from or write to Pinot | The current guide covers distributed scans, column and filter pushdown, SQL support, gRPC streaming reads, and secure connections. |

## How to choose

Choose Flink when Pinot writes are one stage inside a broader Flink DAG and you need the Pinot sink to participate in enrichment or windowing logic. Choose Spark when you want Pinot to integrate with Spark SQL or DataFrame workflows for reads, writes, or hybrid pipelines.

If the goal is primarily to load data into Pinot, start with the ingestion guides instead of a processing connector. If the goal is to move data between Pinot and a processing framework, this is the right place.

## Detailed docs

* [Flink connector](../../integrations/flink-connector.md)
* [Spark-Pinot connector](../../integrations/spark-pinot-connector/README.md)

## What this page covered

This page covered the two processing connectors used when Pinot reads or writes are embedded in Flink or Spark jobs.

## Next step

Open the connector-specific guide and wire the Pinot sink or source into your existing processing job.

## Related pages

* [Client libraries](client-libraries.md)
* [Ingestion](../ingestion/README.md)
* [REST / gRPC APIs](rest-grpc-apis.md)
