---
description: >-
  Learn to build and manage Apache Pinot clusters, uncovering key components for
  efficient data processing and optimized analysis.
---

# Cluster

A Pinot [_cluster_](components/cluster/) is a collection of the software processes and hardware resources required to ingest, store, and process data. For detail about Pinot cluster components, see [Physical architecture](./#physical-architecture).

A Pinot cluster consists of the following processes, which are typically deployed on separate hardware resources in production. In development, they can fit comfortably into Docker containers on a typical laptop:

* **Controller**: Maintains cluster metadata and manages cluster resources.
* **Zookeeper**: Manages the Pinot cluster on behalf of the controller. Provides fault-tolerant, persistent storage of metadata, including table configurations, schemas, segment metadata, and cluster state.
* **Broker**: Accepts queries from client processes and forwards them to servers for processing.
* **Server**: Provides storage for segment files and compute for query processing.
* (Optional) **Minion**: Computes background tasks other than query processing, minimizing impact on query latency. Optimizes segments, and builds additional indexes to ensure performance (even if data is deleted).

The simplest possible Pinot cluster consists of four components: a server, a broker, a controller, and a Zookeeper node. In production environments, these components typically run on separate server instances, and scale out as needed for data volume, load, availability, and latency. Pinot clusters in production range from fewer than ten total instances to more than 1,000.

Pinot uses [Apache Zookeeper](https://zookeeper.apache.org/) as a distributed metadata store and [Apache Helix](http://helix.apache.org/) for cluster management.

Helix is a cluster management solution that maintains a persistent, fault-tolerant map of the intended state of the Pinot cluster. Helix constantly monitors the cluster to ensure that the right hardware resources are allocated for the present configuration. When the configuration changes, Helix schedules or decommissions hardware resources to reflect the new configuration. When elements of the cluster change state catastrophically, Helix schedules hardware resources to keep the actual cluster consistent with the ideal represented in the metadata. From a physical perspective, Helix takes the form of a controller process plus agents running on servers and brokers.

## Cluster configuration

For details of cluster configuration settings, see [Cluster configuration reference](https://docs.pinot.apache.org/configuration-reference/cluster).

## Cluster components

Helix divides nodes into logical components based on their responsibilities:

### Participant

Participants are the nodes that host distributed, partitioned resources

Pinot servers are modeled as participants. For details about server nodes, see [Server](server.md).

### Spectator

Spectators are the nodes that observe the current state of each participant and use that information to access the resources. Spectators are notified of state changes in the cluster (state of a participant, or that of a partition in a participant).

Pinot brokers are modeled as spectators. For details about broker nodes, see [Broker](broker.md).

### Controller

The node that observes and controls the Participant nodes. It is responsible for coordinating all transitions in the cluster and ensuring that state constraints are satisfied while maintaining cluster stability.

Pinot controllers are modeled as controllers. For details about controller nodes, see [Controller](controller.md).

## Logical view

Another way to visualize the cluster is a logical view, where:

* A cluster contains [tenants](tenant.md)
* Tenants contain [tables](../table/)
* Tables contain [segments](../table/segment/)

![](../../../.gitbook/assets/ClusterLogical.jpg)

## Set up a Pinot cluster

Typically, there is only one cluster per environment/data center. There is no need to create multiple Pinot clusters because Pinot supports [tenants](tenant.md).

To set up a cluster, see one of the following guides:

* [Running Pinot in Docker](../../getting-started/running-pinot-in-docker.md)
* [Running Pinot locally](../../getting-started/running-pinot-locally.md)
