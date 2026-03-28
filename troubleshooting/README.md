---
description: Diagnose and resolve issues in Apache Pinot by identifying your problem type and following the right troubleshooting path.
---

# Troubleshooting

Use this page to find the right troubleshooting guide for your situation. Start by identifying the type of problem you are experiencing, then follow the link to the relevant guide.

## What kind of problem are you seeing?

### Query issues

Queries returning errors, unexpected results, or timing out.

| Symptom | Go to |
|---|---|
| `BrokerResourceMissingError`, reserved keyword errors, wrong results, slow queries | [Query FAQ](query-faq.md) |
| Errors or limitations specific to the multi-stage query engine (v2), including type mismatches, unsupported functions, or timeout errors | [Troubleshoot Multi-Stage Query Engine](troubleshoot-multi-stage-query-engine.md) |

### Ingestion issues

Data not appearing, segments stuck, or ingestion pipelines failing.

| Symptom | Go to |
|---|---|
| Segment sizing, partitioning, indexing, Kafka ingestion, data encoding, or real-time ingestion questions | [Ingestion FAQ](ingestion-faq.md) |
| Kafka partitions stopped consuming, segment commit failures, `Controller response was FAILED` errors | [Realtime Ingestion Stopped](realtime-ingestion-stopped.md) |

### Operations and cluster issues

Cluster instability, memory problems, segment errors, rebalancing, or configuration questions.

| Symptom | Go to |
|---|---|
| Heap sizing, backup/restore, schema changes, rebalancing, segment states (BAD/ERROR), tenant configuration, minion tasks, tiered storage | [Operations FAQ](operations-faq.md) |
| Using the debug API, slow query diagnosis, GC pressure on servers | [Troubleshooting Pinot](troubleshooting-pinot.md) |

### Kubernetes issues

Problems specific to running Pinot on Kubernetes.

| Symptom | Go to |
|---|---|
| Increasing server disk size on AWS EKS, PVC resizing, pod restarts | [Pinot on Kubernetes FAQ](pinot-on-kubernetes-faq.md) |

### ZooKeeper issues

ZooKeeper errors related to metadata storage limits.

| Symptom | Go to |
|---|---|
| `packet len is out of range` errors, znode size exceeded, too many segments | [Troubleshoot ZooKeeper](troubleshoot-zookeeper.md) |

### General questions

Broad questions about Pinot architecture and behavior.

| Symptom | Go to |
|---|---|
| How deep storage works, how Pinot uses ZooKeeper, JDK compatibility, timezone configuration | [General FAQ](general-faq.md) |

## Quick diagnostic checklist

Before diving into a specific guide, gather the following information to speed up diagnosis:

1. **Which component is affected?** Controller, broker, server, or minion?
2. **Check the logs.** All Pinot components log error conditions. Look for stack traces or error messages.
3. **Use the debug API.** The [Table Debug API](../users/api/controller-api-reference.md) surfaces common problems including table size, ingestion status, and state transition errors.
4. **Check metrics.** If you have [monitoring](../operators/operating-pinot/monitoring.md) set up, review dashboards for anomalies in query latency, ingestion lag, or GC pressure.
5. **Review recent changes.** Did you recently update a table config, schema, or cluster configuration?

## Related Operate Pinot pages

Many troubleshooting issues connect back to operational configuration and tuning. These pages may help:

* [Deployment and Monitoring](../operators/operating-pinot/README.md) -- overview of operating Pinot clusters
* [Monitoring](../operators/operating-pinot/monitoring.md) -- set up dashboards and alerts to catch issues early
* [Rebalance](../operators/operating-pinot/rebalance/) -- resolve uneven segment distribution or add new servers
* [Segment Lifecycle and Repair](../operators/operating-pinot/segment-lifecycle-and-repair.md) -- understand segment states and repair procedures
* [Decoupling Controller from the Data Path](../operators/operating-pinot/decoupling-controller-from-the-data-path.md) -- reduce controller bottlenecks for real-time ingestion
* [Tuning](../operators/operating-pinot/tuning/) -- optimize query routing, real-time performance, and segment pruning
* [Managing Logs](../operators/operating-pinot/managing-logs.md) -- configure log levels for debugging
* [Upgrading Pinot](../operators/operating-pinot/upgrading-pinot-cluster.md) -- check upgrade notes before and after cluster upgrades
* [Setup Cluster](../operators/operating-pinot/setup-cluster.md) -- verify cluster configuration

## Next step

If you cannot resolve your issue using these guides, reach out to the Apache Pinot community:

* **Slack**: [Join the Apache Pinot Slack](https://inviter.co/apache-pinot) and ask in the troubleshooting channel
* **GitHub Issues**: [apache/pinot](https://github.com/apache/pinot/issues) for bug reports and feature requests
* **Mailing list**: [users@pinot.apache.org](mailto:users@pinot.apache.org) for general questions
