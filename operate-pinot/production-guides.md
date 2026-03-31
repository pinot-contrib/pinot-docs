# Production Guides

This section collects the guides you need to run Apache Pinot reliably in production. It covers topology decisions, capacity planning, health checks, graceful operations, disaster recovery, and operational observability through log management.

## When to use these guides

- You are preparing a Pinot cluster for production traffic.
- You need to plan capacity for servers, brokers, and controllers.
- You want to configure health-check endpoints for load balancers or Kubernetes probes.
- You are setting up graceful shutdown, rolling restarts, or node replacement procedures.
- You need to inspect or change log levels dynamically without restarting components.

## Prerequisites

- A deployed Pinot cluster (see [Deployment](deployment.md) for setup instructions).
- Monitoring infrastructure to collect Pinot metrics (Prometheus, Datadog, or similar).
- Familiarity with your deep store backend (S3, GCS, HDFS) for backup and recovery planning.

## Primary guide

### Running Pinot in Production

[Running Pinot in Production](running-pinot-in-production.md) is the comprehensive production deployment guide. It covers:

- **Cluster topology and prerequisites** -- ZooKeeper, deep store, controllers, brokers, servers, minions, and load balancers.
- **Deployment and upgrade order** -- the correct sequence for rolling out and rolling back component upgrades.
- **Capacity planning** -- sizing servers (disk, memory, query concurrency), brokers (QPS), and controllers.
- **Health checks and SLIs** -- endpoints for every component and recommended service-level indicators for availability, latency, correctness, ingestion freshness, and cluster stability.
- **Graceful operations** -- graceful server shutdown, node replacement with segment predownload, and rolling restarts.
- **Backup and disaster recovery** -- ZooKeeper state backup, deep store durability, and table config versioning.
- **Operational runbooks** -- links to segment lifecycle, rebalance, and real-time ingestion troubleshooting.

### Managing logs

[Managing Logs](../operators/operating-pinot/managing-logs.md) documents the REST APIs for inspecting and changing Log4J log levels at runtime and for downloading log files from any component, including remote log download through the controller. These capabilities are essential for debugging transient production issues without restarting services.

## Next step

For deploying Pinot on Kubernetes with Helm charts, see [Kubernetes Deployment](kubernetes/deployment-pinot-on-kubernetes.md).
