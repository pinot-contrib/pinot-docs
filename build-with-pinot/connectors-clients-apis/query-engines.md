---
description: Connect federated SQL engines to Pinot for cross-source analytics.
---

# Query engines

Use federated query engines when Pinot is one source in a broader SQL stack and you want to join or compare it with other systems. These integrations are the right fit when a data platform already standardizes on Trino or Presto for interactive analytics.

## What belongs here

| Engine | Best for | Notes |
| --- | --- | --- |
| Trino | Interactive federated SQL across multiple data sources | The current guide covers Kubernetes deployment, Pinot catalog configuration, and CLI-based validation. |
| Presto | Federated SQL with Pinot connector support | The current guide covers Docker setup, CLI validation, and Pinot gRPC streaming support for certain connector version ranges. |

## How to choose

Choose Trino when your platform already uses Trino catalogs and you want a connector-oriented path into Pinot. Choose Presto when your organization is already on the Presto ecosystem and needs Pinot to behave like one more SQL source.

The detailed query-engine docs include version-specific connector notes and CLI examples. Keep those versioned examples aligned with the source pages when you update them, especially the Trino and Presto command snippets.

If you are deploying on Kubernetes, start with the Kubernetes query engine guide after you pick Trino or Presto.

## Detailed docs

* [Trino](../../integrations/trino.md)
* [Presto](../../integrations/presto.md)
* [Query engines on Kubernetes](../../basics/getting-started/kubernetes/query-engines.md)

## What this page covered

This page covered the two federated SQL engines most commonly used to query Pinot alongside other systems.

## Next step

Use the linked detail guide for your engine of choice, then verify the catalog or connector configuration with a small query before rolling it into production.

## Related pages

* [BI tools](bi-tools.md)
* [REST / gRPC APIs](rest-grpc-apis.md)
* [Querying Pinot](../querying-and-sql/querying-pinot.md)
