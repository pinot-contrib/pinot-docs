---
description: Overview of the Apache Pinot Maven modules and how the codebase is organized.
---

# Code Modules and Organization

Apache Pinot is a multi-module Maven project. Each module provides specific functionality and can be composed into individually deployable services. This page describes every top-level module in the repository, grouped by architectural layer.

Source code lives under `src/main/java` in each module, with corresponding unit tests under `src/test/java`.

## SPI / Foundation

These modules define the interfaces, data types, and shared utilities that the rest of Pinot depends on. They intentionally have a minimal dependency footprint.

| Module | Description |
| --- | --- |
| `pinot-spi` | Service Provider Interface -- defines plugin contracts for file systems, stream ingestion, input formats, metrics, authentication, and more. All plugin implementations depend on this module. |
| `pinot-segment-spi` | Segment-level SPI -- abstractions for column data sources, readers, and segment metadata used by both local and remote segment implementations. |
| `pinot-common` | Shared classes used across Pinot components including table config definitions, metrics helpers, Zookeeper metadata models, request/response formats, and common utilities. |

## Segment Storage

| Module | Description |
| --- | --- |
| `pinot-segment-local` | Local (on-server) segment implementation -- column index structures (forward index, inverted index, range index, text index, etc.), segment creation, and segment loading logic. |

## Core

| Module | Description |
| --- | --- |
| `pinot-core` | Central module containing single-stage query execution (filters, aggregations, transformations, group-by), real-time segment ingestion, upsert handling, and data-plane utilities shared by Broker and Server. |

## Query Engine (Multi-Stage)

These modules power the multi-stage query engine (V2), which enables distributed joins and other advanced SQL operations.

| Module | Description |
| --- | --- |
| `pinot-query-planner` | SQL query parsing, validation, and logical/physical plan generation using Apache Calcite. Produces a distributed query plan that is split across Broker and Server stages. |
| `pinot-query-runtime` | Execution runtime for multi-stage query plans -- operator implementations, inter-stage data transfer (mailbox), and scheduling of query stages on Broker and Server. |

## Services

Each Pinot service runs as a separate process and corresponds to a Maven module.

| Module | Description |
| --- | --- |
| `pinot-broker` | Broker service -- accepts SQL queries, performs query routing using routing tables, scatters requests to Servers, gathers and merges partial results, and returns the final response. |
| `pinot-controller` | Controller service -- cluster administration APIs, segment management (upload, assignment, retention, rebalance), schema and table configuration, and task scheduling via Helix. |
| `pinot-server` | Server service -- hosts segments, executes query plans on local data, serves real-time and offline segments, and exposes admin REST APIs. |
| `pinot-minion` | Minion service -- runs asynchronous, distributed tasks such as segment merge, segment purge (e.g. GDPR compliance), and segment conversion. Task types are pluggable. |

## Time Series

| Module | Description |
| --- | --- |
| `pinot-timeseries/pinot-timeseries-spi` | SPI for the time series query engine -- defines the language-agnostic interfaces for time series query planning and execution. |
| `pinot-timeseries/pinot-timeseries-planner` | Planner for time series queries -- translates time series language expressions into executable query plans that run on top of Pinot segments. |

Time series language implementations (e.g. M3QL) are provided as plugins under `pinot-plugins/pinot-timeseries-lang`.

## Connectors

The `pinot-connectors` module contains integrations for ingesting data from external compute frameworks.

| Module | Description |
| --- | --- |
| `pinot-spark-common` | Shared code for Spark-based segment generation. |
| `pinot-spark-2-connector` | Connector for Apache Spark 2.x batch segment generation. |
| `pinot-spark-3-connector` | Connector for Apache Spark 3.x batch segment generation. |
| `pinot-flink-connector` | Connector for Apache Flink segment generation and real-time ingestion. |

## Clients

The `pinot-clients` module provides client libraries for querying Pinot from applications.

| Module | Description |
| --- | --- |
| `pinot-java-client` | Native Java client for sending SQL queries to the Broker and reading results. |
| `pinot-jdbc-client` | JDBC driver implementation, allowing Pinot to be used with standard JDBC tooling and BI applications. |
| `pinot-cli` | Command-line interface client for interactive querying. |

## Plugins

The `pinot-plugins` module is an umbrella for all first-party plugin implementations. Plugins are loaded at runtime via the SPI mechanism defined in `pinot-spi`. For details on the plugin architecture, see the [Plugin Architecture](../../developers/plugin-architecture/) section.

| Plugin Group | Submodules | Description |
| --- | --- | --- |
| `pinot-stream-ingestion` | `pinot-kafka-base`, `pinot-kafka-3.0`, `pinot-kafka-4.0`, `pinot-kinesis`, `pinot-pulsar` | Stream connectors for real-time ingestion from Kafka, Kinesis, and Pulsar. |
| `pinot-file-system` | `pinot-s3`, `pinot-gcs`, `pinot-hdfs`, `pinot-adls` | PinotFS implementations for deep store on S3, GCS, HDFS, and Azure Data Lake. |
| `pinot-input-format` | `pinot-avro`, `pinot-json`, `pinot-csv`, `pinot-parquet`, `pinot-orc`, `pinot-thrift`, `pinot-protobuf`, `pinot-arrow`, `pinot-clp-log`, and Confluent schema-registry variants | Record readers/decoders for various data serialization formats. |
| `pinot-batch-ingestion` | `pinot-batch-ingestion-standalone`, `pinot-batch-ingestion-hadoop`, `pinot-batch-ingestion-spark-*` | Ingestion job runners for standalone, Hadoop MapReduce, and Spark-based offline segment generation. |
| `pinot-metrics` | `pinot-yammer`, `pinot-dropwizard`, `pinot-compound-metrics` | Metrics reporter implementations (Yammer, Dropwizard) and compound metric support. |
| `pinot-minion-tasks` | `pinot-minion-builtin-tasks` | Built-in Minion task types (merge/rollup, purge, segment conversion, etc.). |
| `pinot-segment-uploader` | `pinot-segment-uploader-default` | Default segment uploader for pushing completed segments to the Controller. |
| `pinot-segment-writer` | `pinot-segment-writer-file-based` | File-based segment writer implementation used during ingestion. |
| `pinot-environment` | `pinot-azure` | Environment-specific configuration provider for Azure deployments. |
| `pinot-timeseries-lang` | `pinot-timeseries-m3ql` | Time series query language plugins (M3QL). |

## Tools and Distribution

| Module | Description |
| --- | --- |
| `pinot-tools` | Collection of command-line tools for cluster setup, segment management, data generation, and the Pinot quick-start launchers. |
| `pinot-distribution` | Assembly module that packages all modules into the final Pinot binary distribution (tar.gz). |

## Testing and Verification

| Module | Description |
| --- | --- |
| `pinot-integration-test-base` | Base framework and utilities shared by integration tests (cluster setup helpers, test table configs, etc.). |
| `pinot-integration-tests` | End-to-end integration tests that spin up multi-component Pinot clusters and validate cross-module behavior without mocking. |
| `pinot-perf` | JMH-based micro-benchmarks for evaluating performance of critical code paths (index reads, aggregations, encoding). |
| `pinot-compatibility-verifier` | Backward and forward compatibility tests that verify rolling upgrades work across Pinot versions. |
| `pinot-udf-test` | Test harness for validating user-defined scalar and aggregate functions. |
| `pinot-dependency-verifier` | Build-time checks to detect dependency conflicts and enforce dependency convergence. |

## Deployment

These directories are not Maven modules but contain deployment artifacts.

| Directory | Description |
| --- | --- |
| `docker/` | Dockerfiles and supporting scripts for building Pinot container images. |
| `helm/` | Helm charts for deploying Pinot on Kubernetes, including templates for Broker, Controller, Server, Minion, and Zookeeper. |

## Key External Dependencies

Pinot builds on top of several important external projects:

* **Apache Helix / ZooKeeper** -- cluster management, resource assignment, and distributed state coordination.
* **Apache Calcite** -- SQL parsing and query planning for the multi-stage query engine.
* **Apache Kafka** -- default stream provider for real-time ingestion (pluggable via SPI).
* **Netty** -- non-blocking network transport between Broker and Server.
* **Google Guava** -- caches, rate limiters, and general-purpose utilities.
* **RoaringBitmap** -- compressed bitmap library used for inverted indices and filtering.
* **T-Digest** -- quantile estimation for percentile aggregation functions.

## Related pages

* [Code Setup](code-setup.md) -- set up your local development environment and build Pinot from source.
* [Dependency Management](dependency-management.md) -- guidelines for managing Maven dependencies across modules.
* [Extending Pinot](extending-pinot/README.md) -- create custom plugins using the SPI framework.
* [Build Docker Images](../../tutorials/operations/build-docker-images.md) -- package Pinot modules into Docker containers.
