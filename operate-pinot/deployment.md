# Deployment

This section covers everything you need to deploy an Apache Pinot cluster, from bootstrapping your first ZooKeeper-connected cluster through configuring tables, ingestion pipelines, and component-level settings. Use these guides to stand up Pinot in any environment -- bare metal, VMs, or containers -- before moving on to production hardening.

## When to use these guides

- You are deploying Pinot for the first time outside of the quickstart.
- You need to start individual Pinot components (controller, broker, server) with custom configuration files.
- You are setting up tables, schemas, and ingestion jobs against a running cluster.
- You want to optimize your configuration using the recommendation engine or decouple the controller from the real-time data path.

## Prerequisites

- Java 11 or later installed (or Docker if using container-based deployment).
- A running Apache ZooKeeper ensemble (three nodes recommended for production).
- Access to a deep store (local filesystem for development; S3, GCS, HDFS, or ADLS for production).
- The Pinot binary distribution downloaded from [pinot.apache.org/download](https://pinot.apache.org/download) or the official Docker image.

## Child pages

### Cluster setup

[Set up a Pinot cluster](setup-cluster.md) walks through creating a cluster namespace and starting controller, broker, and server instances.

### Advanced Pinot setup

[Advanced Pinot Setup](advanced-pinot-setup.md) provides step-by-step instructions for starting each Pinot component individually using Docker or launcher scripts, configuring components with custom config files, creating batch and streaming tables, and loading data.

### Server startup status checkers

[Server Startup Status Checkers](server-startup-status-checkers.md) explains readiness and liveness health checks, static consumption wait, offset-based and freshness-based segment checkers, and recommended configurations for QA and production environments.

### Table setup

[Set up a table](setup-table.md) links to table creation instructions including schema design, table configuration, and index settings.

### Ingestion setup

[Set up ingestion](setup-ingestion.md) covers creating segments and running batch data ingestion jobs to load data into your tables.

### Decoupling controller from the data path

[Decoupling Controller from the Data Path](decoupling-controller-from-the-data-path.md) explains how to bypass the controller during real-time segment completion by uploading completed segments directly to deep store, and how to enable peer download for failure recovery.

### Command-line interface (CLI)

[CLI Reference](cli.md) documents every `pinot-admin.sh` command -- from `AddSchema` and `AddTable` through `RebalanceTable`, `LaunchDataIngestionJob`, and cluster validation utilities.

### Configuration recommendation engine

[Configuration Recommendation Engine](configuration-recommendation-engine.md) describes the rule-based engine accessible via the controller REST API that recommends optimal index, partitioning, segment size, and real-time provisioning settings based on your schema, query patterns, and workload characteristics.

## Next step

Once your cluster is deployed and serving data, harden it for production use. See [Production Guides](production-guides.md) for capacity planning, health checks, graceful operations, and disaster recovery.
