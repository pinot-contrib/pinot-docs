---
description: >-
  Overview of tools and connectors that integrate with Apache Pinot for querying,
  visualization, data processing, and observability.
---

# Integrations

Apache Pinot integrates with a broad ecosystem of tools for querying, visualization, data ingestion, and observability. This page organizes integrations by category to help you find the right tool for your use case.

## Query Engines

Run federated SQL queries against Pinot alongside other data sources.

| Integration | Description |
| --- | --- |
| [Trino](trino.md) | Distributed SQL query engine with a built-in Pinot connector for interactive analytics across multiple data sources. |
| [Presto](presto.md) | Distributed SQL query engine originally developed at Facebook, with native Pinot connector support. |

## BI & Visualization

Connect dashboarding and exploration tools to Pinot for interactive analytics.

| Integration | Description |
| --- | --- |
| [Superset](superset.md) | Open-source BI platform with a native Pinot connector for building dashboards and running ad hoc queries. |
| [Tableau](tableau.md) | Enterprise BI platform that can connect to Pinot via JDBC for drag-and-drop visual analytics. |
| [Metabase](metabase.md) | Open-source BI tool with a community Pinot driver for self-service analytics and dashboards. |

## Data Processing Connectors

Write data into Pinot programmatically from batch or streaming processing frameworks.

| Integration | Description |
| --- | --- |
| [Flink Connector](flink-connector.md) | Apache Flink sink for writing data directly into Pinot tables. Ideal for backfilling offline tables and bootstrapping upsert tables. |
| [Spark-Pinot Connector](spark-pinot-connector/README.md) | Read data from Pinot into Spark DataFrames and write data back. Supports distributed parallel scans, column/filter pushdown, and gRPC streaming reads. |

## Observability

Monitor and detect anomalies in Pinot data.

| Integration | Description |
| --- | --- |
| [ThirdEye](thirdeye.md) | Anomaly detection and root cause analysis platform designed to work with Pinot time-series data. |
