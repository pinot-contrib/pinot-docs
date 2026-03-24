---
description: Reduce query latency, control resource usage, and scale throughput by tuning routing, scheduling, memory, and real-time ingestion.
---

# Performance Tuning

## Purpose

Pinot query costs vary widely depending on workload characteristics, data distribution, and cluster topology. This section provides the operator-facing knobs for improving latency, throughput, and resource efficiency across a Pinot cluster. Use these guides after your tables are ingesting data and you have baseline metrics to compare against.

## Tuning categories

### Query routing and fanout

Control how brokers select servers and how many servers participate in each query. Reducing unnecessary fanout is the single highest-leverage tuning action for tail latency.

| Page | What it covers |
|---|---|
| [Optimizing Scatter and Gather](routing.md) | Partition pruning, time pruning, replica-group routing, single-replica routing, preferred pool routing, broker tag enforcement |
| [Adaptive Server Selection](query-routing-using-adaptive-server-selection.md) | Route queries to the fastest available server using latency and in-flight request stats |
| [Segment Pruning](segment-pruning.md) | Broker-side and server-side pruning strategies (time, partition, bloom filter, column value) to skip irrelevant segments |

### Query scheduling and resource isolation

Prioritize production traffic over ad-hoc queries and prevent noisy-neighbor problems.

| Page | What it covers |
|---|---|
| [Query Scheduling](query-scheduling.md) | FCFS, bounded FCFS, and token-bucket schedulers for controlling query concurrency on servers |
| [Workload-Based Query Isolation](workload-query-isolation.md) | Binary workload and named-workload schedulers with per-workload CPU and memory budgets |
| [OOM Protection](../oom-protection-using-automatic-query-killing.md) | Heap monitoring and automatic query killing to prevent server out-of-memory crashes |

### Memory and storage

Tune how Pinot maps segment data into memory and controls disk I/O.

| Page | What it covers |
|---|---|
| [Tuning Default MMAP Advice](tuning-default-mmap-advice.md) | Configure `posix_madvise` hints (RANDOM, SEQUENTIAL, WILL_NEED) for memory-mapped segment files |
| [Performance Optimization Configurations](../../../tutorials/operations/performance-optimization-configurations.md) | Predicate reordering, streaming segment download, Netty native TLS and transport |
| [Segment Operations Throttling](../../../tutorials/operations/segment-operations-throttling.md) | Limit parallelism of segment download, index rebuild, and StarTree preprocessing to protect server resources |

### Real-time ingestion tuning

Optimize memory, throughput, and segment sizing for tables consuming from streaming sources.

| Page | What it covers |
|---|---|
| [Tuning Real-time Performance](realtime.md) | Off-heap allocation, consuming segment row thresholds, completed-segment placement, split commit protocol, RealtimeProvisioningHelper |
| [Pauseless Consumption](../pauseless-consumption.md) | Eliminate ingestion pauses during segment commit by consuming into a new segment in parallel with build and upload |
| [Pause Ingestion Based on Resource Utilization](../pause-ingestion-based-on-resource-utilization.md) | Automatically pause and resume real-time ingestion when disk utilization exceeds a threshold |

## Where to start

1. **Measure first.** Collect baseline query latency (p50, p95, p99), `numSegmentsQueried`, `numDocsScanned`, and server CPU/memory utilization before changing any configuration.
2. **Reduce fanout.** Enable time and partition pruning, and consider replica-group routing if your table spans many servers.
3. **Right-size consuming segments.** Use the `RealtimeProvisioningHelper` to choose optimal segment sizes and flush thresholds for real-time tables.
4. **Protect production traffic.** Enable adaptive server selection and consider workload isolation if ad-hoc queries share the same cluster.
5. **Tune memory mapping.** On Linux, experiment with `RANDOM` madvise if your workload is point-lookup heavy, or keep the default if scans dominate.
