---
description: Overview of the Apache Pinot Maven modules and how the codebase is organized.
---

# Code Modules and Organization

Apache Pinot is a multi-module Maven project. Each module provides specific functionality and can be composed into individually deployable services. This page describes every top-level module in the repository, grouped by architectural layer.

Source code lives under `src/main/java` in each module, with corresponding unit tests under `src/test/java`.

## SPI / Foundation

These modules define the interfaces, data types, and shared utilities that the rest of Pinot depends on. They intentionally have a minimal dependency footprint.

<table>
  <thead>
    <tr>
      <th>Module</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`pinot-spi`</td>
      <td>Service Provider Interface -- defines plugin contracts for file systems, stream ingestion, input formats, metrics, authentication, and more. All plugin implementations depend on this module.</td>
    </tr>
    <tr>
      <td>`pinot-segment-spi`</td>
      <td>Segment-level SPI -- abstractions for column data sources, readers, and segment metadata used by both local and remote segment implementations.</td>
    </tr>
    <tr>
      <td>`pinot-common`</td>
      <td>Shared classes used across Pinot components including table config definitions, metrics helpers, Zookeeper metadata models, request/response formats, and common utilities.</td>
    </tr>
  </tbody>
</table>

## Segment Storage

<table>
  <thead>
    <tr>
      <th>Module</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`pinot-segment-local`</td>
      <td>Local (on-server) segment implementation -- column index structures (forward index, inverted index, range index, text index, etc.), segment creation, and segment loading logic.</td>
    </tr>
  </tbody>
</table>

## Core

<table>
  <thead>
    <tr>
      <th>Module</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`pinot-core`</td>
      <td>Central module containing single-stage query execution (filters, aggregations, transformations, group-by), real-time segment ingestion, upsert handling, and data-plane utilities shared by Broker and Server.</td>
    </tr>
  </tbody>
</table>

## Query Engine (Multi-Stage)

These modules power the multi-stage query engine (V2), which enables distributed joins and other advanced SQL operations.

<table>
  <thead>
    <tr>
      <th>Module</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`pinot-query-planner`</td>
      <td>SQL query parsing, validation, and logical/physical plan generation using Apache Calcite. Produces a distributed query plan that is split across Broker and Server stages.</td>
    </tr>
    <tr>
      <td>`pinot-query-runtime`</td>
      <td>Execution runtime for multi-stage query plans -- operator implementations, inter-stage data transfer (mailbox), and scheduling of query stages on Broker and Server.</td>
    </tr>
  </tbody>
</table>

## Services

Each Pinot service runs as a separate process and corresponds to a Maven module.

<table>
  <thead>
    <tr>
      <th>Module</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`pinot-broker`</td>
      <td>Broker service -- accepts SQL queries, performs query routing using routing tables, scatters requests to Servers, gathers and merges partial results, and returns the final response.</td>
    </tr>
    <tr>
      <td>`pinot-controller`</td>
      <td>Controller service -- cluster administration APIs, segment management (upload, assignment, retention, rebalance), schema and table configuration, and task scheduling via Helix.</td>
    </tr>
    <tr>
      <td>`pinot-server`</td>
      <td>Server service -- hosts segments, executes query plans on local data, serves real-time and offline segments, and exposes admin REST APIs.</td>
    </tr>
    <tr>
      <td>`pinot-minion`</td>
      <td>Minion service -- runs asynchronous, distributed tasks such as segment merge, segment purge (e.g. GDPR compliance), and segment conversion. Task types are pluggable.</td>
    </tr>
  </tbody>
</table>

## Time Series

<table>
  <thead>
    <tr>
      <th>Module</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`pinot-timeseries/pinot-timeseries-spi`</td>
      <td>SPI for the time series query engine -- defines the language-agnostic interfaces for time series query planning and execution.</td>
    </tr>
    <tr>
      <td>`pinot-timeseries/pinot-timeseries-planner`</td>
      <td>Planner for time series queries -- translates time series language expressions into executable query plans that run on top of Pinot segments.</td>
    </tr>
  </tbody>
</table>

Time series language implementations (e.g. M3QL) are provided as plugins under `pinot-plugins/pinot-timeseries-lang`.

## Connectors

The `pinot-connectors` module contains integrations for ingesting data from external compute frameworks.

<table>
  <thead>
    <tr>
      <th>Module</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`pinot-spark-common`</td>
      <td>Shared code for Spark-based segment generation.</td>
    </tr>
    <tr>
      <td>`pinot-spark-3-connector`</td>
      <td>Connector for Apache Spark 3.x batch segment generation.</td>
    </tr>
    <tr>
      <td>`pinot-flink-connector`</td>
      <td>Connector for Apache Flink segment generation and real-time ingestion.</td>
    </tr>
  </tbody>
</table>

## Clients

The `pinot-clients` module provides client libraries for querying Pinot from applications.

<table>
  <thead>
    <tr>
      <th>Module</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`pinot-java-client`</td>
      <td>Native Java client for sending SQL queries to the Broker and reading results.</td>
    </tr>
    <tr>
      <td>`pinot-jdbc-client`</td>
      <td>JDBC driver implementation, allowing Pinot to be used with standard JDBC tooling and BI applications.</td>
    </tr>
    <tr>
      <td>`pinot-cli`</td>
      <td>Command-line interface client for interactive querying.</td>
    </tr>
  </tbody>
</table>

## Plugins

The `pinot-plugins` module is an umbrella for all first-party plugin implementations. Plugins are loaded at runtime via the SPI mechanism defined in `pinot-spi`. For details on the plugin architecture, see the [Plugin Architecture](../../developers/plugin-architecture/) section.

<table>
  <thead>
    <tr>
      <th>Plugin Group</th>
      <th>Submodules</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`pinot-stream-ingestion`</td>
      <td>`pinot-kafka-base`, `pinot-kafka-3.0`, `pinot-kafka-4.0`, `pinot-kinesis`, `pinot-pulsar`</td>
      <td>Stream connectors for real-time ingestion from Kafka, Kinesis, and Pulsar.</td>
    </tr>
    <tr>
      <td>`pinot-file-system`</td>
      <td>`pinot-s3`, `pinot-gcs`, `pinot-hdfs`, `pinot-adls`</td>
      <td>PinotFS implementations for deep store on S3, GCS, HDFS, and Azure Data Lake.</td>
    </tr>
    <tr>
      <td>`pinot-input-format`</td>
      <td>`pinot-avro`, `pinot-json`, `pinot-csv`, `pinot-parquet`, `pinot-orc`, `pinot-thrift`, `pinot-protobuf`, `pinot-arrow`, `pinot-clp-log`, and Confluent schema-registry variants</td>
      <td>Record readers/decoders for various data serialization formats.</td>
    </tr>
    <tr>
      <td>`pinot-batch-ingestion`</td>
      <td>`pinot-batch-ingestion-standalone`, `pinot-batch-ingestion-hadoop`, `pinot-batch-ingestion-spark-*`</td>
      <td>Ingestion job runners for standalone, Hadoop MapReduce, and Spark-based offline segment generation.</td>
    </tr>
    <tr>
      <td>`pinot-metrics`</td>
      <td>`pinot-yammer`, `pinot-dropwizard`, `pinot-compound-metrics`</td>
      <td>Metrics reporter implementations (Yammer, Dropwizard) and compound metric support.</td>
    </tr>
    <tr>
      <td>`pinot-minion-tasks`</td>
      <td>`pinot-minion-builtin-tasks`</td>
      <td>Built-in Minion task types (merge/rollup, purge, segment conversion, etc.).</td>
    </tr>
    <tr>
      <td>`pinot-segment-uploader`</td>
      <td>`pinot-segment-uploader-default`</td>
      <td>Default segment uploader for pushing completed segments to the Controller.</td>
    </tr>
    <tr>
      <td>`pinot-segment-writer`</td>
      <td>`pinot-segment-writer-file-based`</td>
      <td>File-based segment writer implementation used during ingestion.</td>
    </tr>
    <tr>
      <td>`pinot-environment`</td>
      <td>`pinot-azure`</td>
      <td>Environment-specific configuration provider for Azure deployments.</td>
    </tr>
    <tr>
      <td>`pinot-timeseries-lang`</td>
      <td>`pinot-timeseries-m3ql`</td>
      <td>Time series query language plugins (M3QL).</td>
    </tr>
  </tbody>
</table>

## Tools and Distribution

<table>
  <thead>
    <tr>
      <th>Module</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`pinot-tools`</td>
      <td>Collection of command-line tools for cluster setup, segment management, data generation, and the Pinot quick-start launchers.</td>
    </tr>
    <tr>
      <td>`pinot-distribution`</td>
      <td>Assembly module that packages all modules into the final Pinot binary distribution (tar.gz).</td>
    </tr>
  </tbody>
</table>

## Testing and Verification

<table>
  <thead>
    <tr>
      <th>Module</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`pinot-integration-test-base`</td>
      <td>Base framework and utilities shared by integration tests (cluster setup helpers, test table configs, etc.).</td>
    </tr>
    <tr>
      <td>`pinot-integration-tests`</td>
      <td>End-to-end integration tests that spin up multi-component Pinot clusters and validate cross-module behavior without mocking.</td>
    </tr>
    <tr>
      <td>`pinot-perf`</td>
      <td>JMH-based micro-benchmarks for evaluating performance of critical code paths (index reads, aggregations, encoding).</td>
    </tr>
    <tr>
      <td>`pinot-compatibility-verifier`</td>
      <td>Backward and forward compatibility tests that verify rolling upgrades work across Pinot versions.</td>
    </tr>
    <tr>
      <td>`pinot-udf-test`</td>
      <td>Test harness for validating user-defined scalar and aggregate functions.</td>
    </tr>
    <tr>
      <td>`pinot-dependency-verifier`</td>
      <td>Build-time checks to detect dependency conflicts and enforce dependency convergence.</td>
    </tr>
  </tbody>
</table>

## Deployment

These directories are not Maven modules but contain deployment artifacts.

<table>
  <thead>
    <tr>
      <th>Directory</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`docker/`</td>
      <td>Dockerfiles and supporting scripts for building Pinot container images.</td>
    </tr>
    <tr>
      <td>`helm/`</td>
      <td>Helm charts for deploying Pinot on Kubernetes, including templates for Broker, Controller, Server, Minion, and Zookeeper.</td>
    </tr>
  </tbody>
</table>

## Key External Dependencies

Pinot builds on top of several important external projects:

* **Apache Helix / ZooKeeper** -- cluster management, resource assignment, and distributed state coordination.
* **Apache Calcite** -- SQL parsing and query planning for the multi-stage query engine.
* **Apache Kafka** -- default stream provider for real-time ingestion (pluggable via SPI).
* **Netty** -- non-blocking network transport between Broker and Server.
* **Google Guava** -- caches, rate limiters, and general-purpose utilities.
* **RoaringBitmap** -- compressed bitmap library used for inverted indices and filtering.
* **T-Digest** -- quantile estimation for percentile aggregation functions.
