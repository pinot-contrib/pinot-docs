---
description: Production deployment guide covering topology, capacity, health checks, graceful operations, backups, and rollouts.
---

# Running Pinot in Production

This page covers the operational concerns you should address before running Apache Pinot in a production environment. It focuses on topology decisions, capacity planning, availability, graceful operations, and disaster recovery. For metrics and alerting, see [Monitoring](../operators/operating-pinot/monitoring.md). For upgrade procedures, see [Upgrading Pinot](../operators/operating-pinot/upgrading-pinot-cluster.md).

## Cluster topology and prerequisites

A production Pinot cluster requires the following infrastructure:

**ZooKeeper.** Pinot uses Apache ZooKeeper (via Apache Helix) for cluster coordination, segment metadata, and state management. Dedicate a ZK path for each Pinot cluster by setting `pinot.zk.server` and `pinot.cluster.name` so that multiple Pinot clusters sharing the same ZK ensemble are isolated from each other. Use a ZK ensemble of at least three nodes for quorum resilience.

**Deep store.** Every cluster needs a shared deep store for segment files. Pinot provides PinotFS implementations for Amazon S3, Google Cloud Storage, Azure Data Lake Storage Gen2, HDFS, and local filesystems. Configure the deep store via `pinot.controller.storage.factory.class` and the corresponding filesystem-specific properties. All servers and controllers must be able to read from and write to the deep store.

**Controllers.** Run at least two controllers for leader-election failover. Controllers manage table metadata, segment assignments, and periodic validation tasks. If controllers share a local filesystem for temp segment storage, that filesystem must be shared (or use a PinotFS-backed deep store instead).
**Brokers.** Run at least two brokers behind an HTTP load balancer. Brokers receive queries, compute routing, scatter requests to servers, and merge results. Scale brokers based on query throughput (QPS).

**Servers.** Servers store segments on local disk and execute query plans. Size servers based on the total data footprint, replication factor, and query concurrency. Separate offline and real-time workloads onto different tenants when their resource profiles differ significantly.

**Minions (optional).** Minions run background tasks such as segment merge, purge, and refresh. Deploy minions when you use any Minion task type. Minions are stateless and can be scaled independently.

**Load balancers.** Place HTTP load balancers in front of both brokers (for query traffic) and controllers (for admin API and segment push traffic).

## Deployment and upgrade order

When deploying or upgrading Pinot components, follow this order to avoid protocol or compatibility issues during the rollout:

1. Controller
2. Broker
3. Server
4. Minion

When rolling back, reverse the order (Minion → Server → Broker → Controller). Each component connects to ZooKeeper independently, so the ordering is a best-practice precaution rather than a hard dependency.

For detailed upgrade testing with the cross-version compatibility suite, see [Upgrading Pinot](../operators/operating-pinot/upgrading-pinot-cluster.md).
## Capacity planning

### Servers

Server capacity is driven by three factors: disk footprint, memory, and query concurrency.

**Disk.** Estimate the total segment size across all tables (accounting for the replication factor) and provision at least 1.5× that amount for headroom during rebalance, segment refresh, and temporary copies.

**Memory.** Pinot maps segment data into memory. For offline segments, the JVM heap handles metadata while `mmap` or off-heap buffers serve data pages. For real-time segments, allocate additional off-heap memory (`-XX:MaxDirectMemorySize`) for consuming segments. A common starting point is 4–8 GB heap and 2–4× the consuming-segment footprint for direct memory.

**Query concurrency.** Server thread pools (`pinot.server.netty.worker.threads`, `pinot.server.query.executor.pruner.threadCount`) should be sized to the expected concurrent query load. Monitor `SCHEDULER_WAIT` time to detect saturation.

### Brokers

Broker capacity is primarily driven by QPS and result-set merge cost. Each broker instance can typically handle 500–2,000 QPS depending on query complexity. Monitor `QUERY_QUOTA_CAPACITY_UTILIZATION_RATE` to decide when to scale.

### Controllers

Controllers are lightweight relative to brokers and servers. Two controllers are sufficient for most clusters. Add more only if you observe high API latency or segment-push bottlenecks.
## Health checks and SLIs

Every Pinot component exposes health-check endpoints for use in load-balancer probes, Kubernetes readiness/liveness checks, and monitoring:

| Component | Endpoints |
|---|---|
| Controller | `GET /health` |
| Broker | `GET /health` |
| Server | `GET /health`, `GET /health/liveness`, `GET /health/readiness` |
| Minion | `GET /health` |

All endpoints return HTTP 200 when healthy and 503 when unhealthy.

### Recommended service-level indicators

Define SLIs around these dimensions and alert when they breach your thresholds:

**Query availability.** `PERCENT_SEGMENTS_AVAILABLE` should be 100% per table. Any drop means some segments have no online replica.

**Query latency.** Track the broker-side `QUERY_EXECUTION` timer at p50, p95, and p99. Set SLO thresholds based on your application's latency budget.

**Query correctness.** `BROKER_RESPONSES_WITH_PARTIAL_SERVERS_RESPONDED` and `BROKER_RESPONSES_WITH_PROCESSING_EXCEPTIONS` should be near zero. Sustained non-zero values indicate data gaps in query results.

**Ingestion freshness.** For real-time tables, `REALTIME_INGESTION_DELAY_MS` should stay within your freshness SLA (commonly under 5 minutes). `LLC_PARTITION_CONSUMING = 0` on any partition is a critical alert.

**Cluster stability.** `SEGMENTS_IN_ERROR_STATE > 0`, `HELIX_ZOOKEEPER_RECONNECTS > 1/hour`, and `LLC_STREAM_DATA_LOSS > 0` all warrant investigation.

For the full metrics catalog, alert thresholds, and diagnosis patterns, see [Monitoring](../operators/operating-pinot/monitoring.md).
## Graceful operations

### Graceful server shutdown

Pinot servers support graceful shutdown to drain queries and deregister from the cluster before stopping. The shutdown sequence:

1. The server sets a `shutdownInProgress` flag in Helix, signaling brokers to stop routing new queries to it.
2. If `pinot.server.shutdown.enableQueryCheck` is enabled (default: true), the server waits for in-flight queries to complete.
3. If `pinot.server.shutdown.enableResourceCheck` is enabled (default: true), the server waits for external-view convergence.
4. The shutdown times out after `pinot.server.shutdown.timeoutMs` (default: 600,000 ms / 10 minutes).

Configure a process-manager stop timeout (for example, Kubernetes `terminationGracePeriodSeconds`) that is at least as long as the server shutdown timeout.

### Graceful server node replacement

On cloud platforms, node replacement is common. Pinot supports predownloading segments to the replacement node before the original node is stopped, making the replacement overhead comparable to a restart rather than a full segment download.

**Workflow:**

1. Start the new node in predownload mode using the `PredownloadScheduler`. It downloads all immutable segments for the instance and makes its disk state identical to the original node.
2. Wait for predownload to complete (fully or partially after sufficient retries).
3. Stop the original node.
4. Start the new node in normal mode.

The new node must be assigned the same `instanceId` as the original. Predownload parallelism is controlled by `pinot.server.predownload.parallelism` (defaults to `numProcessors × 3`).
### Rolling restarts

When restarting all servers (for example, for a JVM configuration change), restart them one at a time and wait for external-view convergence between each restart. This ensures that at least `replication - 1` replicas remain available for every segment throughout the process. Use the `/health/readiness` endpoint to gate each restart.

## Backup and disaster recovery

### ZooKeeper state

Pinot stores all cluster metadata — table configs, schemas, segment assignments, and ideal state — in ZooKeeper. Back up ZooKeeper data regularly using ZK's native snapshot mechanism or a tool like `zkCopy`. In a disaster, restoring ZK from a snapshot and restarting controllers restores the cluster metadata.

### Deep store segments

The deep store is the authoritative copy of all segment data. Ensure your deep-store backend (S3, GCS, HDFS) has its own durability and backup strategy (for example, S3 versioning or cross-region replication). If a server loses local segment files, it re-downloads them from deep store automatically on startup or via a reload with `forceDownload=true`.

### Table config and schema versioning

Store table configs and schemas in version control alongside your deployment manifests. This makes it straightforward to recreate tables if ZK state is lost and provides an audit trail of configuration changes.

## Operational runbooks

For day-to-day segment operations — choosing between reset, reload, refresh, rebalance, force commit, and Minion repair tasks — see the [Segment Lifecycle and Repair](../operators/operating-pinot/segment-lifecycle-and-repair.md) runbook.

For rebalancing after capacity changes, see [Rebalance](../operators/operating-pinot/rebalance/README.md).

For managing real-time ingestion issues, see the [Real-time Ingestion Stopped](operate-pinot/troubleshooting/realtime-ingestion-stopped.md) troubleshooting guide.
## Further reading

- [Monitoring](../operators/operating-pinot/monitoring.md) — metrics, alert thresholds, and diagnosis patterns
- [Upgrading Pinot](../operators/operating-pinot/upgrading-pinot-cluster.md) — upgrade order and compatibility testing
- [Segment Lifecycle and Repair](../operators/operating-pinot/segment-lifecycle-and-repair.md) — when to reset vs. reload vs. refresh vs. rebalance
- [Kubernetes Deployment](kubernetes/deployment-pinot-on-kubernetes.md) — Helm-based deployment on Kubernetes
- [Helm Chart Values Reference](kubernetes/helm-chart-reference.md) — all configurable Helm values
- [Performance Tuning](../operators/operating-pinot/tuning/README.md) — query routing, scheduling, and segment pruning