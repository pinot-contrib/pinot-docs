---
description: End-to-end guides for canonical Apache Pinot workloads.
---

# Workload Playbooks

The rest of the Pinot documentation covers individual features: schema design, ingestion modes, indexes, query syntax, and operational knobs. These playbooks stitch those features together into **complete, production-ready patterns** for the workloads adopters ask about most often.

Each playbook covers:

| Section | What it answers |
| --- | --- |
| **When to use this pattern** | Is this the right fit for my workload? |
| **Architecture sketch** | Which Pinot components are involved and how data flows |
| **Schema and table config** | Concrete JSON you can adapt |
| **Ingestion setup** | Stream and/or batch job configuration |
| **Indexing strategy** | Which indexes to enable and why |
| **Query patterns** | Representative SQL and performance tips |
| **Operational checklist** | Monitoring, scaling, and common pitfalls |

## Playbooks

| Playbook | Typical use case |
| --- | --- |
| [Real-Time Product Analytics](real-time-product-analytics.md) | Sub-second dashboards over Kafka event streams (page views, clicks, transactions) |
| [CDC / Upsert Pipeline](cdc-upsert-pipeline.md) | Keep Pinot in sync with a transactional database via Debezium and upserts |
| [Hybrid Real-Time + Offline](hybrid-offline-realtime.md) | Combine low-latency streaming with high-quality batch backfills in a single logical table |
| [Multi-Tenant Analytics](multi-tenant-analytics.md) | Serve many customers from one Pinot cluster with resource and data isolation |
| [Text Search Analytics](text-search-analytics.md) | Full-text search over logs, product catalogs, or support tickets alongside OLAP aggregations |

## How to use these playbooks

1. **Pick the playbook** closest to your workload.
2. **Copy the configs** and adjust field names, topic names, and resource sizes for your environment.
3. **Cross-reference the feature docs** linked inside each playbook for deep dives on any single capability.
4. **Check the operational checklist** before going to production.

{% hint style="info" %}
These playbooks target Pinot 1.x and assume familiarity with [Pinot's architecture](../basics/architecture.md) and [table types](../basics/components/table/README.md). If you are new to Pinot, start with the [10-Minute Quickstart](../basics/getting-started/ten-minute-quickstart.md) first.
{% endhint %}
